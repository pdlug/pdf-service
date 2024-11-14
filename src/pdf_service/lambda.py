from mangum import Mangum

import pdf_service.api as api

handler = Mangum(api.app)
