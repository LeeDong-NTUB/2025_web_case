from web_case_2025.models.BusinessInfo import BusinessInfo

def business_info(request):
    return {
        'business_info': BusinessInfo.objects.first()
    }
