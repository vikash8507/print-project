class Voter(models.Model):
    epic = models.CharField(max_length=20, unique=True)
    name1 = models.CharField(max_length=100)
    name2 = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    blck1 = models.CharField(max_length=100)
    blck2 = models.CharField(max_length=100, default="")
    subblock = models.CharField(max_length=100)
    address1 = models.CharField(max_length=250, blank=True, null=True)
    address2 = models.CharField(max_length=250, blank=True, null=True)
    gender = models.CharField(max_length=100)
    birth = models.DateField(null=True, blank=True)
    gname1 = models.CharField(max_length=100)
    gname2 = models.CharField(max_length=100)
    partno = models.CharField(max_length=100)
    partname1 = models.CharField(max_length=100)
    partname2 = models.CharField(max_length=100, default="")
    serialno = models.CharField(max_length=100)
    guardian_title = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='photos/', default="voter.png")
    barcode = models.ImageField(upload_to='barcodes/', null=True, blank=True)

    def __str__(self):
        return self.epic
