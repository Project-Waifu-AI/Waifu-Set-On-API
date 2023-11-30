from fastapi import APIRouter

# BecomeWaifu
from api.action.BecomWaifu import router as router_bw

# AsistenWaifu
from api.action.AsistenWaifu import router as router_aiu

# auth wso
from api.autentikasi.wso_auth import router as router_wso_auth

# auth google
from api.autentikasi.google_auth import router as router_google_auth

# admin access
from tambahan.admin_access import router as router_admin

# CRUD user
from tambahan.user_set import router as router_user

router = APIRouter(prefix='/api')

# router bw
router.include_router(router_bw)

# router aiu
router.include_router(router_aiu)

# router auth wso
router.include_router(router_wso_auth)

# router auth google
router.include_router(router_google_auth)

# router admin access
router.include_router(router_admin)

# router crud user
router.include_router(router_user)