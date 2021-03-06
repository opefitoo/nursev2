# -*- coding: utf-8 -*-

import datetime

from models import Patient, InvoiceItem, Prestation, PrivateInvoiceItem
from django.http import HttpResponseRedirect

def previous_months_invoices_october(modeladmin, request, queryset):
    # response = HttpResponse(content_type='text')

    previous_month_patients = Patient.objects.raw("select p.id, p.name, p.first_name " +
                                                  "from public.invoices_patient p, public.invoices_prestation prest " +
                                                  "where p.id = prest.patient_id " +
                                                  "and prest.date between '2014-10-01'::DATE and '2014-10-31'::DATE " +
                                                  "and p.private_patient = 'f' " +
                                                  "and (select count(inv.id) from public.invoices_invoiceitem inv " +
                                                  "where inv.invoice_date between '2014-10-01'::DATE and '2014-10-31'::DATE " +
                                                  "and inv.patient_id = p.id) = 0" +
                                                  "group by p.id " +
                                                  "order by p.name")
    invoice_counters = 0
    for p in previous_month_patients:
        invoiceitem = InvoiceItem(patient=p,
                                  invoice_date=datetime.datetime(2014, 10, 31),
                                  invoice_sent=False,
                                  invoice_paid=False)
        invoiceitem.clean()
        invoiceitem.save()
        invoice_counters = invoice_counters + 1

def previous_months_invoices_april(modeladmin, request, queryset):
    # response = HttpResponse(content_type='text')

    previous_month_patients = Patient.objects.raw("select p.id, p.name, p.first_name " +
                                                  "from public.invoices_patient p, public.invoices_prestation prest " +
                                                  "where p.id = prest.patient_id " +
                                                  "and prest.date >= '2015-04-01'and prest.date <= '2015-04-30' " +
                                                  "and p.private_patient = 'f' " +
                                                  "and (select count(inv.id) from public.invoices_invoiceitem inv " +
                                                  "where inv.invoice_date between '2015-04-01'::DATE and '2015-04-30'::DATE " +
                                                  "and inv.patient_id = p.id) = 0" +
                                                  "group by p.id " +
                                                  "order by p.name")
    invoice_counters = 0
    for p in previous_month_patients:
        invoiceitem = InvoiceItem(patient=p,
                                  invoice_date=datetime.datetime(2015, 04, 30),
                                  invoice_sent=False,
                                  invoice_paid=False)
        invoiceitem.clean()
        invoiceitem.save()
        invoice_counters = invoice_counters + 1

def previous_months_invoices_june(modeladmin, request, queryset):
    # response = HttpResponse(content_type='text')

    previous_month_patients = Patient.objects.raw("select p.id, p.name, p.first_name " +
                                                  "from public.invoices_patient p, public.invoices_prestation prest " +
                                                  "where p.id = prest.patient_id " +
                                                  "and prest.date >= '2015-06-01'and prest.date <= '2015-06-30' " +
                                                  "and p.private_patient = 'f' " +
                                                  "and (select count(inv.id) from public.invoices_invoiceitem inv " +
                                                  "where inv.invoice_date between '2015-06-01'::DATE and '2015-06-30'::DATE " +
                                                  "and inv.patient_id = p.id) = 0" +
                                                  "group by p.id " +
                                                  "order by p.name")
    invoice_counters = 0
    for p in previous_month_patients:
        invoiceitem = InvoiceItem(patient=p,
                                  invoice_date=datetime.datetime(2015, 06, 30),
                                  invoice_sent=False,
                                  invoice_paid=False)
        invoiceitem.clean()
        invoiceitem.save()
        invoice_counters = invoice_counters + 1

def create_invoice(modeladmin, request, queryset):
    # response = HttpResponse(content_type='text')

    not_invoiced_prestas = Prestation.objects.raw("select p.id,p.patient_id,p.carecode_id,p.date" +
                                                  " from invoices_prestation p " +
                                                  "left join invoices_invoiceitem_prestations ip on p.id = ip.prestation_id " +
                                                  "where ip.prestation_id is NULL")
    from collections import defaultdict

    prestations_to_invoice = defaultdict(list)
    invoices_created = []
    invpks = []
    for p in queryset:
        if p in not_invoiced_prestas:
            prestations_to_invoice[p.patient].append(p)

    for k, v in prestations_to_invoice.iteritems():
        if (k.private_patient):
            invoiceitem = PrivateInvoiceItem(private_patient=k,
                                             invoice_date=datetime.datetime.now(),
                                             invoice_sent=False,
                                             invoice_paid=False)
        else:
            invoiceitem = InvoiceItem(patient=k,
                                      invoice_date=datetime.datetime.now(),
                                      invoice_sent=False,
                                      invoice_paid=False)
            invoices_created.append(invoiceitem)
            invpks.append(invoiceitem.pk)
        invoiceitem.save()
        for prestav in v:
            invoiceitem.prestations.add(prestav)

    #return HttpResponseRedirect("/admin/invoices/invoiceitem/?ct=%s&ids=%s" % (invoiceitem.pk, ",".join(invpks)))
    return HttpResponseRedirect("/admin/invoices/invoiceitem/")
