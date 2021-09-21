from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required

import os
from django.conf import settings
from lxml import etree

import code128
from datetime import date
from main.models import Voter
from main.forms import VoterForm

@login_required
def upload_voter(request):
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
        code128.image(epic).save(os.path.join(
            path, f"{epic}.png"))
        sp = block.split(" ")
        spblock = f'{sp[2]} {sp[1]} {sp[0]}'
        voter_data = Voter(
            epic=epic,
            name1=name1,
            name2=name2,
            state=state,
            blck1=spblock,
            subblock=subblock,
            gender=gender,
            gname1=gname1,
            gname2=gname2,
            partname1=partname,
            partno=partno,
            serialno=serialno,
            barcode=f"barcodes/{epic}.png",
            guardian_title=guardian_title.split('/')[1].strip()
        )
        voter_data.save()
        messages.success(
            request, "Voter card added successfully. Please update it before print.")
        return redirect("voters-list")
    return render(request, 'main/upload-voter.html')

@login_required
def fill_voter(request, id):
    voter = get_object_or_404(Voter, id=id)
    if request.method == "POST":
        add1 = request.POST.get("add1", voter.address1)
        add2 = request.POST.get("add2", voter.address2)
        birth = request.POST.get("birth", voter.birth)
        blck1 = request.POST.get("blck1", voter.blck1)
        blck2 = request.POST.get("blck2", voter.blck2)
        partname1 = request.POST.get("partname1", voter.partname1)
        partname2 = request.POST.get("partname2", voter.partname2)
        photo = request.FILES.get("photo", voter.photo)
        if add1 == 'None' or add2 == 'None' or photo == '' or birth == '':
            messages.warning(
                request, "Please update address1, address2, date of birth and photo")
        else:
            voter.address1 = add1
            voter.address2 = add2
            voter.photo = photo
            voter.birth = birth
            voter.blck1 = blck1
            voter.blck2 = blck2
            voter.partname2 = partname2
            voter.partname2 = partname2
            voter.save()
            messages.success(request, "Voter updated")
            return redirect("voters-list")
    context = {
        "voter": voter,
    }
    return render(request, 'main/fill-voter.html', context)

@login_required
def delete_voter(request, id):
    voter = get_object_or_404(Voter, id=id)
    voter.delete()
    messages.success(request, "Voter deleted successfully.")
    return redirect("voters-list")

@login_required
def voters_list(request):
    voters = Voter.objects.all()
    return render(request, 'main/voters.html', {'voters': voters})

@login_required
def generate_pdf(request, id):
    voter = get_object_or_404(Voter, id=id)
    if voter.address1 == '' or voter.address2 == '' or voter.birth == '' or voter.photo == '':
        messages.warning(request, "Please update Address, Birth and Image.")
        return redirect(f"/fill-voter/{voter.id}")
    context = {
        "voter": voter,
        "date": date.today().strftime("%d/%m/%Y")
    }
    return render(request, "voter.html", context)
