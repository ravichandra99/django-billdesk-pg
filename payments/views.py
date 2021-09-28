from django.shortcuts import render
from payments.forms import checkoutForm
from payments.models import Transaction,Amount
from django.contrib.auth.models import User
from payments.responseMsg import ResponseMessage
from payments.gen_message import GetMessage
import uuid
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import hashlib
from django.contrib.auth.decorators import login_required
# from django.core.mail import send_mail
from django.utils.text import slugify

# Create your views here.
#function to get unique order_id
def get_order_id(id):
    return str(id)+str(uuid.uuid4())[:8]

#function to generate message and send to billdesk

def payment_request(request):
    if request.method == 'POST':
        form = checkoutForm(request.POST)
        if form.is_valid():
            amount = 0
            email_id = slugify(form.cleaned_data['email'])
            if User.objects.filter(id = request.user.id).exists():
                usr_details = User.objects.filter(id = request.user.id)
                usr_details = usr_details[0]
                fname = slugify(usr_details.username)
                id = usr_details.pk
                mnumber = '9885098850'  #assuming u have a another table called User with mob_number as a field
                while True:
                    oid = get_order_id(id) 
                    #we use a combo of user's id and uuid to generate a unique order_id
                    #we use this in a loop and check the genrated the order_i with existing ones in the db
                    #to make sure its unique
                    trans = Transaction.objects.filter(order_id=oid)
                    if not trans:
                        break
                if Amount.objects.filter(pk = 1).exists():
                    amount = Amount.objects.all().first().amount
                else:
                    amount = 10.00
                msg = GetMessage().message(oid, amount, id, email_id, fname, mnumber)
                Transaction.objects.create(owner=usr_details, order_id=oid, email=usr_details.email, amount_initiated=amount, status='PENDING', registered_for='transfer', log=str([msg]), txn_date=timezone.localtime(timezone.now()))
                return render(request, 'paymentProcess.html', {'msg': msg, 'url': settings.BILL_URL})
            else:
                usr_details = User.objects.filter(id = request.user.id)
                id = 12345
                mnumber = '9885098850'
                fname = 'sampleuser'
                while True:
                    oid = get_order_id(id) 
                    #we use a combo of user's id and uuid to generate a unique order_id
                    #we use this in a loop and check the genrated the order_i with existing ones in the db
                    #to make sure its unique
                    trans = Transaction.objects.filter(order_id=oid)
                    if not trans:
                        break
                if Amount.objects.filter(pk = 1).exists():
                    amount = Amount.objects.all().first().amount
                else:
                    amount = 10.00
                msg = GetMessage().message(oid, amount, id, email_id, fname, mnumber)
                Transaction.objects.create(owner=None, order_id=oid, email=email_id, amount_initiated=amount, status='PENDING', registered_for='transfer', log=str([msg]), txn_date=timezone.localtime(timezone.now()))
                return render(request, 'paymentProcess.html', {'msg': msg, 'url': settings.BILL_URL})

    form = checkoutForm()
    return render(request, 'paymentspage.html', {'form': form})


@csrf_exempt
def handleResponse(request):
    if request.method=='POST':
        response = request.POST
        v = ResponseMessage()
        values = v.respMsg(response)
        server_to_server(response)
        if values and values['MID']==settings.MID:
            transac = Transaction.objects.filter(order_id=values['OrderID'])[0]
            tstat,amnt,txnid,dnt,mode = values['TStat'],values['AMNT'], values['TaxnNo'],values['DnT'],values['TMode']
            email = values['Email']
            if tstat == '0300' and transac.amount_initiated==float(amnt):
                    id = transac.owner.id
                    reg_for = str(transac.registered_for)
                    usr_details = User.objects.filter(id=id)[0]
                    typ = 'success'
                    msgs = ['Success','Payment Succesful', reg_for]
                    # send_mail(
                    #          'DTEAPENGG TRANSFER PAYMENT',
                    #          'Your payment of Rs.{} was successful'.format(amnt),
                    #          settings.DEFAULT_FROM_EMAIL,
                    #          [email],
                    #          fail_silently=False,
                    #          )
            elif tstat == '0300' and transac.amount_initiated!=amnt:
                reg_for = str(transac.registered_for)
                #transac.status = 'AMOUNT Tampered'
                #transac.was_success = False
                msgs = ['Failed', 'Payment declined! Looked liked someone tried tampering your payment',reg_for]
                typ='danger'
            elif tstat == '0002':
                reg_for = str(transac.registered_for)
                msgs = ['Failed', 'Billdesk is waiting for the trasaction status from your bank. Will update you as soon as we have any response',reg_for]
                typ = 'info'
            elif tstat != '0300':
                reg_for = str(transac.registered_for)
                if tstat == '0399':
                    detail = 'Invalid Authentication at Bank'
                elif tstat == 'NA':
                    detail = 'Invalid Input in the Request Message'
                elif tstat =='0001':
                    detail = 'error at billdesk'
                else:
                    detail = 'Payment Failed'
                    
                msgs = ['Failed', detail, reg_for]
                typ = 'danger'
                transac.log += str([response])
                #transac.status = "FAILED"
            else:
                return HttpResponse('Bad Request')

            transac.ru_date = timezone.localtime(timezone.now())
            transac.save()
            return render(request, 'afterPayment.html', {'error': msgs, 'typ':typ, 'txnid':txnid, 'date':dnt, 'amnt': amnt, 'mode':mode})
        else:
            msgs = ['Failed','Payment declined! Looked liked someone tried tampering your payment']
            return render(request, 'afterPayment.html', {'error': msgs, 'typ': 'danger'})
    else:
        return HttpResponse('Bad Request')


def server_to_server(response):
        v = ResponseMessage()
        values = v.respMsg(response)
        if values and values['MID']==settings.MID:
            transac = Transaction.objects.filter(order_id=values['OrderID'])[0]
            tstat,amnt,txnid,dnt,mode = values['TStat'],values['AMNT'], values['TaxnNo'],values['DnT'],values['TMode']
            transac.txn_id = txnid
            if tstat == '0300' and transac.amount_initiated==float(amnt):
                transac.status = 'SUCCESS'
                id = transac.owner.id
                reg_for = str(transac.registered_for)
                usr_details = User.objects.filter(id=id)[0]
                transac.was_success = True
            elif tstat == '0300' and transac.amount_initiated!=amnt:
                transac.status = 'AMOUNT Tampered'
                transac.was_success = False
            elif tstat != '0300' and tstat == '0002':
                transac.status = "WAITING"
            elif tstat != '0300' and tstat != '0002':
                transac.status = "FAILED"
            transac.log += str([response])
            transac.s2s_date = timezone.localtime(timezone.now())
            transac.save()
