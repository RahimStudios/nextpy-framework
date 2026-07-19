def get_template():
    """Return the template to render"""
    return "debug_ssr_test.html"


def getServerSideProps(context):
    """SSR data fetching function"""
    return {
        "props": {
            "title": "SSR Test - NextPy Framework"
        }
    }
