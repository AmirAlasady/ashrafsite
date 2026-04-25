from .models import FooterInfo


def site_context(request):
    return {
        "footer": FooterInfo.objects.first(),
    }
