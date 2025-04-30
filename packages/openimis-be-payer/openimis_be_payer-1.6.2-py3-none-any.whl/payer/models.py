import uuid
import itertools
from django.conf import settings
from core import models as core_models
from django.db import models
from django.utils.translation import gettext as _
from product.models import Product

class PayerType(models.Model):
    code = models.CharField(db_column="Code", primary_key=True, max_length=1)
    payer_type = models.CharField(db_column="PayerType", max_length=50)
    alt_language = models.CharField(
        db_column="AltLanguage", max_length=50, blank=True, null=True
    )
    sort_order = models.IntegerField(db_column="SortOrder", blank=True, null=True)

    class Meta:
        managed = True
        db_table = "tblPayerType"


class Payer(core_models.VersionedModel):
    PAYER_TYPE_COOP = "C"
    PAYER_TYPE_DONOR = "D"
    PAYER_TYPE_GOV = "G"
    PAYER_TYPE_LOCAL_AUTH = "L"
    PAYER_TYPE_OTHER = "O"
    PAYER_TYPE_PRIVATE_ORG = "P"
    PAYER_TYPE_CHOICES = (
        (PAYER_TYPE_COOP, "Co-operative"),
        (PAYER_TYPE_DONOR, "Donor"),
        (PAYER_TYPE_GOV, "Government"),
        (PAYER_TYPE_LOCAL_AUTH, "Local Authority"),
        (PAYER_TYPE_OTHER, "Other"),
        (PAYER_TYPE_PRIVATE_ORG, "Private Organization"),
    )

    id = models.AutoField(db_column="PayerID", primary_key=True)
    uuid = models.CharField(
        db_column="PayerUUID", max_length=36, default=uuid.uuid4, unique=True
    )
    type = models.CharField(
        db_column="PayerType", max_length=1, choices=PAYER_TYPE_CHOICES
    )
    name = models.CharField(db_column="PayerName", max_length=100, null=False)
    address = models.CharField(
        db_column="PayerAddress", max_length=100, null=True, blank=True
    )
    location = models.ForeignKey(
        "location.Location",
        db_column="LocationId",
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
        related_name="+",
    )
    phone = models.CharField(db_column="Phone", max_length=50, null=True, blank=True)
    fax = models.CharField(db_column="Fax", max_length=50, null=True, blank=True)
    email = models.CharField(db_column="eMail", max_length=50, null=True, blank=True)

    audit_user_id = models.IntegerField(db_column="AuditUserID")

    # rowid = models.TextField(db_column='RowID', blank=True, null=True)

    @classmethod
    def get_queryset(cls, queryset, user):
        from location.models import LocationManager

        queryset = cls.filter_queryset(queryset)
        if settings.ROW_SECURITY and not user._u.is_imis_admin:
            queryset = LocationManager().build_user_location_filter_query(user._u, queryset = Payer.objects, loc_types=['R', 'D'])
        return queryset

    class Meta:
        managed = True
        db_table = "tblPayer"

class Funding(core_models.HistoryModel):
    class FundingStatus(models.TextChoices):
        PENDING = "N", _("PENDING")
        PAID = "P", _("PAID")
        AWAITING_FOR_RECONCILIATION = "A", _("AWAITING_FOR_RECONCILIATION")
        RECONCILIATED = "R", _("RECONCILIATED")

    product = models.ForeignKey(Product,
                                models.DO_NOTHING, db_column='ProdID',
                                blank=True, null=True,
                                related_name="fundings")
    amount = models.DecimalField(
        db_column='Amount', max_digits=18, decimal_places=2, blank=True, null=True)
    pay_date = models.DateField(
        db_column='PaidDate', blank=True, null=True)
    status = models.CharField(
        db_column='Status', max_length=1, choices=FundingStatus.choices, default=FundingStatus.PENDING, null=False
    )
    payer = models.ForeignKey(
        Payer,
        models.DO_NOTHING,
        db_column="PayerID",
        blank=True,
        null=True,
        related_name="fundings",
    )
    receipt = models.CharField(db_column="Receipt", max_length=50)
    
    class Meta:
        managed = True
        db_table = "tblFunding"
        
class PayerMutation(core_models.UUIDModel, core_models.ObjectMutation):
    payer = models.ForeignKey(Payer, models.DO_NOTHING, related_name="+")
    mutation = models.ForeignKey(
        core_models.MutationLog, models.DO_NOTHING, related_name="payers"
    )

    class Meta:
        managed = True
        db_table = "payer_PayerMutation"
