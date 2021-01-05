import sys


def wsSat(ws):

	results = False

	if ws == "autenticacion":
		results = "https://cfdidescargamasivasolicitud.clouda.sat.gob.mx/Autenticacion/Autenticacion.svc"
	elif ws == "solicitud":
		results = "https://cfdidescargamasivasolicitud.clouda.sat.gob.mx/SolicitaDescargaService.svc"
	elif ws == "verificacion":
		results = "https://cfdidescargamasivasolicitud.clouda.sat.gob.mx/VerificaSolicitudDescargaService.svc"
	elif ws == "descarga":
		results = "https://cfdidescargamasiva.clouda.sat.gob.mx/DescargaMasivaService.svc"

	return results