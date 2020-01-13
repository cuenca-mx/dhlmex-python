from typing import Dict

dhl_urls: Dict[str, str] = {
    'login': '/jsp/app/login/login.xhtml',
    'home': '/jsp/app/inicio/inicio.xhtml',
    'guide': '/jsp/app/cliente/impresionClienteSubUsuario.xhtml',
    'capture': '/jsp/app/cliente/capturaDatosImpresionClienteSU.xhtml',
    'print': '/jsp/app/cliente/guiasImpresas.xhtml',
    'pdf': '/generaImpresionPDF',
}

actions: Dict[str, Dict[str, str]] = {
    'close': {
        'text': 'Cerrar Sesión',
        'code': 'j_id9:j_id26',
        'end': 'j_id9:j_id30',
    },
    'print': {
        'text': 'Impresión Sub Usuario',
        'code': 'j_id9:j_id14',
        'end': 'j_id9:j_id16',
    },
}
