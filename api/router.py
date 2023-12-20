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

# user root websocket
from api.websocket.user import router as socket_user

# premium regis
from api.premium.premium_regis import router as router_premium_regis

# DelusionWaifu
from api.action.DelusionWaifu import router as router_dw

router = APIRouter(prefix='/api')

# router bw
router.include_router(router_bw)

# router aiu
router.include_router(router_aiu)

# router delusionwaifu
router.include_router(router_dw)

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

# socket crud user
router.include_router(socket_user)

# router premium regis
router.include_router(router_premium_regis)