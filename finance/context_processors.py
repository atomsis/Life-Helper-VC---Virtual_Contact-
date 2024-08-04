from .models import UserBalance

def user_balance(request):
    balance = 0.00
    if request.user.is_authenticated:
        try:
            balance = UserBalance.objects.get(user=request.user).balance
        except UserBalance.DoesNotExist:
            balance = 0.00
    return {'user_balance': balance}