from .models import Category

def categories(reqeust):
    return{
        'categories': Category.objects.all()
    }