from fastapi import APIRouter

# BecomeWaifu
from api.action.BecomWaifu import router as router_bw

# AsistenWaifu
from api.action.AsistenWaifu import router as router_aiu

# websocket aiu
from api.websocket.aiu import router as socket_aiu

# auth wso
from api.autentikasi.wso_auth import router as router_wso_auth

# auth google
from api.autentikasi.google_auth import router as router_google_auth

# auth smd
from api.autentikasi.smd_auth import router as router_smd_auth

# admin access
from api.tambahan.admin_access import router as router_admin

# user root
from api.tambahan.user_root import router as router_user

# premium regis
from api.premium.premium_regis import router as router_premium_regis

router = APIRouter(prefix='/api')

# router bw
router.include_router(router_bw)

# router aiu
router.include_router(router_aiu)

# socket aiu
router.include_router(socket_aiu)

# router auth wso
router.include_router(router_wso_auth)

# router auth google
router.include_router(router_google_auth)

# router auth wso
router.include_router(router_smd_auth)

# router admin access
router.include_router(router_admin)

# router crud user
router.include_router(router_user)

# router premium regis
router.include_router(router_premium_regis)