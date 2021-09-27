from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

import razorpay
import os
from django.conf import settings
from lxml import etree
from englisttohindi.englisttohindi import EngtoHindi

import code128
from datetime import date
from main.models import Voter, Payment, PANCard
from .const import PAY_AMOUNTS, POINTS_AMOUNTS

def protect_access(request):
    return request.user.points <= 0

@login_required
def dashboard(request):
    context = {
        "points": request.user.points,
        "voters": Voter.objects.filter(user=request.user).count(),
        "pans": PANCard.objects.filter(user=request.user).count()
    }
    if request.method == 'POST':
        points = request.POST.get('points')
        amount = PAY_AMOUNTS[points] * 100

        key = "rzp_live_xhED2BBdkcvIAm"
        secret = "wAPuZzHFnXCw3sXsCRpDNfaO"

        client = razorpay.Client(auth=(key, secret))
        order_currency = 'INR'

        payment = client.order.create(data={"amount": amount, "currency": order_currency})

        new_payment = Payment(
            razorpay_order_id=payment['id'],
            amount=float(PAY_AMOUNTS[points]),
            user=request.user
        )
        new_payment.save()
        context['payment'] = payment
        context['key'] = key
        return render(request, 'main/dashboard.html', context)
    return render(request, 'main/dashboard.html', context)

@login_required
@csrf_exempt
def success(request):
    if request.method == 'GET':
        messages.warning(request, 'You can not access.')
        return redirect('dashboard')
    razorpay_order_id = request.POST.get("razorpay_order_id")
    payment = Payment.objects.filter(razorpay_order_id=razorpay_order_id).first()
    if payment.paid:
        messages.success(request, "Payment completed")
        return redirect("dashboard")
    payment.paid = True
    payment.save()
    user = payment.user
    user.points = user.points + POINTS_AMOUNTS[str(int(payment.amount))]
    user.save()
    context = {
        "oreder_id": payment.razorpay_order_id,
        "user": payment.user,
        "amount": payment.amount,
        "status": 'success',
        "timestamp": payment.created
    }
    return render(request, 'main/success.html', context)

@login_required
def upload_voter(request):
    if protect_access(request):
        messages.warning(request, "You have no points to take any print.")
        return redirect("dashboard")

    if request.method == 'POST':
        data = request.FILES.get('voter', None)
        if not data:
            return render(request, 'main/upload-voter.html')
        soup = BeautifulSoup(data, 'lxml')
        voter = etree.HTML(str(soup))
        state = voter.xpath(
            '//*[@id="ng-app"]/body/div[4]/div/div[1]/form/table/tbody/tr[2]/td[2]')[0].text
        block = voter.xpath(
            '//*[@id="ng-app"]/body/div[4]/div/div[1]/form/table/tbody/tr[3]/td[2]')[0].text
        subblock = voter.xpath(
            '//*[@id="ng-app"]/body/div[4]/div/div[1]/form/table/tbody/tr[4]/td[2]')[0].text
        name1 = voter.xpath(
            '//*[@id="ng-app"]/body/div[4]/div/div[1]/form/table/tbody/tr[6]/td')[0].text
        name2 = voter.xpath(
            '//*[@id="ng-app"]/body/div[4]/div/div[1]/form/table/tbody/tr[5]/td[2]')[0].text
        gender = voter.xpath(
            '//*[@id="ng-app"]/body/div[4]/div/div[1]/form/table/tbody/tr[7]/td[2]')[0].text
        epic = voter.xpath(
            '//*[@id="ng-app"]/body/div[4]/div/div[1]/form/table/tbody/tr[8]/td[2]')[0].text
        gname1 = voter.xpath(
            '//*[@id="ng-app"]/body/div[4]/div/div[1]/form/table/tbody/tr[10]/td')[0].text
        gname2 = voter.xpath(
            '//*[@id="ng-app"]/body/div[4]/div/div[1]/form/table/tbody/tr[9]/td[2]')[0].text
        partno = voter.xpath(
            '//*[@id="ng-app"]/body/div[4]/div/div[1]/form/table/tbody/tr[11]/td[2]')[0].text
        partname = voter.xpath(
            '//*[@id="ng-app"]/body/div[4]/div/div[1]/form/table/tbody/tr[12]/td[2]')[0].text
        serialno = voter.xpath(
            '//*[@id="ng-app"]/body/div[4]/div/div[1]/form/table/tbody/tr[13]/td[2]')[0].text
        polling_station = voter.xpath(
            '//*[@id="ng-app"]/body/div[4]/div/div[1]/form/table/tbody/tr[14]/td[2]')[0].text
        guardian_title = voter.xpath(
            '//*[@id="ng-app"]/body/div[4]/div/div[1]/form/table/tbody/tr[9]/td[1]')[0].text
        
        if Voter.objects.filter(epic=epic).exists():
            messages.warning(request, "This voter card is already downloaded.")
            return redirect('voters-list')

        path = settings.BASE_DIR / "media/barcodes/"
        code128.image(epic).save(os.path.join(path, f"{name1+gname1}.png"))
        sp = block.split(" ")
        spblock = f'{sp[2]} {sp[1]} {sp[0]}'
        blck2 = f"{sp[2]} {sp[1]} {EngtoHindi(sp[0]).convert}"
        partname2 = EngtoHindi(partname).convert
        voter_data = Voter(
            epic=epic,
            name1=name1,
            name2=name2,
            state=state,
            blck1=spblock,
            blck2=blck2,
            subblock=subblock,
            gender=gender,
            gname1=gname1,
            gname2=gname2,
            partname1=partname,
            partname2=partname2,
            partno=partno,
            serialno=serialno,
            barcode=f"barcodes/{name1+gname1}.png",
            guardian_title=guardian_title.split('/')[1].strip(),
            user=request.user,
        )
        voter_data.save()
        user = request.user
        user.points = user.points - 1
        user.save()
        messages.success(
            request, "Voter card added successfully. Please update it before print.")
        return redirect("voters-list")
    return render(request, 'main/upload-voter.html')

@login_required
def fill_voter(request, id):
    if protect_access(request):
        messages.warning(request, "You have no points to take any print.")
        return redirect("dashboard")
    voter = get_object_or_404(Voter, id=id)
    if request.method == "POST":
        add1 = request.POST.get("add1", voter.address1)
        add2 = request.POST.get("add2", voter.address2)
        birth = request.POST.get("birth", voter.birth)
        blck2 = request.POST.get("blck2", voter.blck2)
        partname2 = request.POST.get("partname2", voter.partname2)
        photo = request.FILES.get("photo", voter.photo)
        
        if add1 == 'None' or add1 == '' or photo == '' or birth == '':
            messages.warning(
                request, "Please update address1, address2, date of birth and photo")
        else:
            voter.address1 = add1
            voter.address2 = add2
            voter.photo = photo
            voter.birth = birth
            voter.blck2 = blck2
            voter.partname2 = partname2
            voter.partname2 = partname2
            voter.save()
            messages.success(request, "Voter updated. Please check and return to voters list")
    context = {
        "voter": voter
    }
    if voter.address2 == "None" or voter.address2 == "":
        res = EngtoHindi(voter.address1).convert
        context['address2'] = res
    return render(request, 'main/fill-voter.html', context)

@login_required
def delete_voter(request, id):
    if protect_access(request):
        messages.warning(request, "You have no points to take any print.")
        return redirect("dashboard")

    voter = get_object_or_404(Voter, id=id)
    voter.delete()
    messages.success(request, "Voter deleted successfully.")
    return redirect("voters-list")

@login_required
def voters_list(request):
    if protect_access(request):
        messages.warning(request, "You have no points to take any print.")
        return redirect("dashboard")
    voters = Voter.objects.all()
    return render(request, 'main/voters.html', {'voters': voters})

@login_required
def generate_pdf(request, id):
    if protect_access(request):
        messages.warning(request, "You have no points to take any print.")
        return redirect("dashboard")
    voter = get_object_or_404(Voter, id=id)
    if voter.address1 == '' or voter.address2 == '' or voter.birth == '' or voter.photo == '':
        messages.warning(request, "Please update Address, Birth and Image.")
        return redirect(f"/fill-voter/{voter.id}")
    context = {
        "voter": voter,
        "date": date.today().strftime("%d/%m/%Y")
    }
    return render(request, "voter.html", context)


@login_required
def pan_list(request):
    if protect_access(request):
        messages.warning(request, "You have no points to take any print.")
        return redirect("dashboard")
    pans = PANCard.objects.all()
    return render(request, "main/pan-list.html", {'pans': pans})

@login_required
def new_pan(request):
    if protect_access(request):
        messages.warning(request, "You have no points to take any print.")
        return redirect("dashboard")
    if request.method == 'POST':
        name = request.POST.get('name')
        fname = request.POST.get('fname')
        birth = request.POST.get('birth')
        pan = request.POST.get('pan')
        photo = request.FILES.get('photo')
        sign = request.FILES.get('sign')
        new_pan = PANCard(
            pan=pan,
            name=name,
            fname=fname,
            birth=birth,
            photo=photo,
            sign=sign,
            user=request.user
        )
        new_pan.save()
        user = request.user
        user.points = user.points - 1
        user.save()
        messages.success(request, "PAN card created successfully.")
        return redirect('pan-list')
    return render(request, "main/new-pan.html")

@login_required
def pan_pdf(request, pk):
    if protect_access(request):
        messages.warning(request, "You have no points to take any print.")
        return redirect("dashboard")
    pan = get_object_or_404(PANCard, pk=pk)
    return render(request, "pan.html", {'pan': pan})