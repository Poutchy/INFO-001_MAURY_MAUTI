import socket
import ssl

import requests
import urllib3
from requests.exceptions import RequestException, SSLError

# Pour éviter l'avertissement dans le test "sans certificat"
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL = "https://www.mauryco.fr"
CA_CERT_PATH = "/etc/pki/ca-trust/source/anchors/root-ca-lorne.pem"
CA_ERROR_PATH = "/etc/pki/ca-trust/source/anchors/error-ca-lorne.pem"


def print_tls_info(hostname, port=443):
    """Affiche les informations TLS : version et cipher suite"""
    context = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                print("=== Informations TLS ===")
                print(f"Version TLS      : {ssock.version()}")
                print(f"Cipher Suite     : {ssock.cipher()}")
                print(f"Certificat serveur : {ssock.getpeercert()['subject']}")
                print("-----------------------------------\n")
    except Exception as e:
        print("Impossible de récupérer les infos TLS :", e)
        print("-----------------------------------\n")


def test_https_connection_without_certificat():
    print("=== Test de connexion HTTPS SANS certificat ===")
    print(f"→ Serveur : {URL}")
    print("-----------------------------------")

    try:
        response = requests.get(URL, timeout=5, verify=False)
        print("Vérification désactivée — certificat accepté sans contrôle.")
        print(f"Code HTTP : {response.status_code}")
        print(f"Réponse du serveur :\n{response.text[:200]}...")
        print_tls_info("www.mauryco.fr")  # Affiche TLS même sans certificat

    except RequestException as req_error:
        print("Erreur réseau ou HTTP :", req_error)
        print("-----------------------------------\n")


def test_https_connection():
    print("=== Test de connexion HTTPS AVEC certificat valide ===")
    print(f"→ Serveur : {URL}")
    print(f"→ Certificat CA utilisé : {CA_CERT_PATH}")
    print("-----------------------------------")

    try:
        response = requests.get(URL, verify=CA_CERT_PATH, timeout=5)
        print("Authentification réussie : le certificat du serveur est valide.")
        print(f"Code HTTP : {response.status_code}")
        print(f"Réponse du serveur :\n{response.text[:200]}...")
        print_tls_info("www.mauryco.fr")  # Affiche TLS

    except SSLError as ssl_error:
        print("Échec de la vérification SSL :", ssl_error)
    except RequestException as req_error:
        print("Erreur réseau ou HTTP :", req_error)


def test_https_connection_with_false_certificat():
    print("=== Test de connexion HTTPS AVEC faux certificat ===")
    print(f"→ Serveur : {URL}")
    print(f"→ Certificat CA utilisé : {CA_ERROR_PATH}")
    print("-----------------------------------")

    try:
        response = requests.get(URL, verify=CA_ERROR_PATH, timeout=5)
        print("Authentification réussie : certificat accepté (inattendu).")
        print(f"Code HTTP : {response.status_code}")
        print(f"Réponse du serveur :\n{response.text[:200]}...")
        print_tls_info("www.mauryco.fr")

    except SSLError as ssl_error:
        print("Échec de la vérification SSL :", ssl_error)
    except RequestException as req_error:
        print("Erreur réseau ou HTTP :", req_error)


if __name__ == "__main__":
    test_https_connection_without_certificat()
    test_https_connection()
    test_https_connection_with_false_certificat()
