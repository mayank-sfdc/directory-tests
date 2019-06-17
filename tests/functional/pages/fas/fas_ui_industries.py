# -*- coding: utf-8 -*-
"""FAS - Industries page"""
import logging

from requests import Response, Session

from tests import URLs
from tests.functional.pages import Services
from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Services.FAS
NAME = "Industries"
TYPE = "listing"
URL = URLs.FAS_INDUSTRIES.absolute
EXPECTED_STRINGS = [
    "FIND THE BEST UK SUPPLIERS FOR YOUR INDUSTRY",
    "More industries",
]
EXPECTED_STRINGS_HEALTH = [
    "Healthcare and life sciences in the UK",
    (
        "Get access to the UK health and life sciences supply-chain, delivering "
        "high quality, innovative services to the world."
    ),
    "Find out more about the UK’s healthcare and life sciences",
]
EXPECTED_STRINGS_TECHNOLOGY = [
    "The UK's advanced technology",
    (
        "Check out the cutting-edge technological innovations that the UK is "
        "bringing to the world."
    ),
    "Find out more about UK technology",
]
EXPECTED_STRINGS_CREATIVE = [
    "The UK's creative services",
    (
        "Whether you need buildings designed, films made or a fresh approach to "
        "marketing, the UK is the first place to look."
    ),
    "Find out more about the UK’s creative services",
]
EXPECTED_STRINGS_FOOD_AND_DRINK = [
    "The UK's food and drink",
    (
        "Whether you want the best food brands or exceptional quality drinks, the"
        " UK should be first on your list."
    ),
    "Find out more about UK food and drink",
]

INDUSTRY_NAMES = {
    "english": [
        "aerospace",
        "agritech",
        "automotive",
        "business & government partnerships",
        "consumer & retail",
        "creative services",
        "cyber security",
        "education",
        "energy",
        "engineering",
        "food and drink",
        "healthcare",
        "infrastructure",
        "innovation",
        "legal services",
        "life sciences",
        "marine",
        "professional & financial services",
        "space",
        "sports economy",
        "technology",
    ],
    "german": [
        "agrartechnologie",
        "automobilbranche",
        "bildung",
        "cybersicherheit",
        "einzelhandel",
        "energie",
        "finanz- und fachdienstleistungen",
        "gesundheitsversorgung",
        "handels- und regierungspartnerschaften",
        "infrastruktur",
        "ingenieurwesen",
        "innovation",
        "kreativbranche",
        "lebensmittel und getränke",
        "life sciences",
        "luft- und raumfahrt",
        "marine und schifffahrt",
        "raumfahrt",
        "rechtsdienstleistungen",
        "sportwirtschaft",
        "technologie",
    ],
    "french": [
        "aéronautique",
        "agritech",
        "automobile",
        "partenariats entre les entreprises",
        "commerce de détail",
        "industries créatives",
        "cybersécurité",
        "éducation",
        "énergie",
        "ingénierie",
        "produits alimentaires et boissons",
        "santé",
        "infrastructures",
        "innovation",
        "services juridiques",
        "sciences de la vie",
        "maritime",
        "services professionnels et financiers",
        "espace",
        "économie du sport",
        "technologie",
    ],
    "chinese": [
        "体育经济",
        "农业技术",
        "创意产业",
        "创新",
        "医疗保健",
        "商业和政府伙伴关系",
        "基础设施",
        "太空业",
        "工程",
        "教育",
        "汽车",
        "法律服务",
        "海事",
        "消费品零售",
        "生命科学",
        "科技",
        "网络安全",
        "能源",
        "航空航天",
        "食品与饮料",
    ],
    "japanese": [
        "アグリテック",
        "イノベーション",
        "インフラストラクチャー",
        "エネルギー",
        "エンジニアリング",
        "クリエイティブ",
        "サイバーセキュリティ",
        "スポーツ経済",
        "テクノロジー",
        "ライフサイエンス",
        "医療サービス",
        "宇宙",
        "専門サービスと金融サービス",
        "教育",
        "法律サービス",
        "海事",
        "消費者小売",
        "産官協力",
        "自動車",
        "航空宇宙",
        "飲食料品",
    ],
    "portuguese": [
        "aeroespacial",
        "tecnologias agrícolas",
        "automotivo",
        "parcerias",
        "varejo consumidor",
        "indústrias criativas",
        "segurança cibernética",
        "educação",
        "energia",
        "engenharia",
        "alimentos e bebidas",
        "assistência médica",
        "infraestrutura",
        "inovação",
        "serviços legais",
        "ciências da vida",
        "marítimo",
        "serviços profissionais e financeiros",
        "espacial",
        "economia esportiva",
        "tecnologia",
    ],
    "spanish": [
        "aeroespacial",
        "agrotecnología",
        "automotriz",
        "colaboración público-privada",
        "venta al por menor",
        "sectores creativos",
        "seguridad cibernética",
        "enseñanza",
        "energía",
        "ingeniería",
        "alimentos y bebidas",
        "sanidad",
        "infraestructura",
        "innovación",
        "servicios jurídicos",
        "ciencias biológicas",
        "marítimo",
        "servicios profesionales y financieros",
        "espacio",
        "economía del deporte",
        "tecnología",
    ],
    "arabic": [
        "صناعة الفضاء الجوي",
        "التقنية الزراعية",
        "صناعة السيارات",
        "الشراكات الحكومية والتجارية",
        "التجزئة للمستهلك",
        "الصناعات الإبداعية",
        "الأمن السيبراني",
        "لتعليم",
        "الطاقة",
        "الهندسة",
        "الطعام والشراب",
        "العناية الصحية",
        "البنية التحتية",
        "الابتكار",
        "الخدمات القانونية",
        "علوم الحياة",
        "الخدمات البحرية",
        "الخدمات المالية والمهنية",
        "لفضاء",
        "الاقتصاد الرياضي",
        "التقنية",
    ],
}


def go_to(session: Session) -> Response:
    headers = {"Referer": URLs.FAS_LANDING.absolute}
    return make_request(Method.GET, URL, session=session, headers=headers)


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Supplier is on FAS Industries page")


def should_see_links_to_industry_pages(response: Response, language: str):
    industry_links = INDUSTRY_NAMES[language.lower()]
    check_response(response, 200, body_contains=industry_links)
