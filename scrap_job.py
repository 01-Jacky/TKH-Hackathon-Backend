import requests
import json
from bs4 import BeautifulSoup
from bs4.element import NavigableString

TEST_URL = 'https://www.indeed.com/viewjob?cmp=Koyfin&t=Senior+Data+Engineer&jk=3433a03b05a7415c&sjdu=QwrRXKrqZ3CNX5W-O9jEvUUdXQhhKNOAMcM5flKILoi8Wcg95REeNW2UC3eKQXgOm7yNS9qrk25LbsaDIY_YIg&tk=1f4i4r55ht57n801&adid=363332321&ad=-6NYlbfkN0A2_1vI8fwFeZf0vK--yNgA55z5N7Pf91wxu5Qw_sXhd2yCBj2hKph-nbPSpGmIsCLGnvbSrpJpJUziDzvYPag1vepmU9_JuiGJYDbuYh-Rd3Im7EKx78-y5CxYwK6X1IUj5zMGO2ipHr-dmUYUsdhM38XIkgyltihs6DEGnj1jL5gaIIyCo7Svdz2plHsOVdQvmzYfhQTmV2aelsf0sH6BCM_z8j3uVHX8t1uVX8orRd1FP3gBFRBRdeytG94Cxc9BzpeL2M65pM74Xs47s'
TEST_2 = "https://www.indeed.com/viewjob?jk=c632d67548fbdbae&q=data+engineer&l=New+York%2C+NY&tk=1f4i8h8ou3og3001&from=web&advn=2089891622738549&adid=258202704&ad=-6NYlbfkN0BR3ykMnr3Vw97HK5IC0i9Uo32NXohanwqRY-CI8z69bhgeevNMD5QwngToFV7LqAOkmOJK17cd_ZJv0-ZfOOgXOC3SdExPh9ZPAoryLuAtatLotpriFJrGoEfQBhh3D3honRT_PBMybCVmqWhiXCNW93cByRB9Lioq13O8ZlCbKkzd_XOQJ1pCusKTRg_H4zNkhhelY47HOtMFcyBCXK4sDXNYF32FogisK7kS4gWEVuLUltuaCexP5z4GXtOStrQGPOocY0UEfQ7MuztkPI6pFYlOOIXgUKLp_ZIf-flh6TmTN1mtejYcDmWZO2vC5u_Tuq_Rs3Z2qQ%3D%3"

response = requests.get(TEST_2)
content = response.content

soup = BeautifulSoup(content, 'html.parser')

# Title and company section
title = soup.find("h1", {"class": "icl-u-xs-mb--xs icl-u-xs-mt--none jobsearch-JobInfoHeader-title"}).text
company = soup.find("div", {"class": "icl-u-lg-mr--sm icl-u-xs-mr--xs"}).text

# Job detail section
job_type = None
try:
    job_details_tree = soup.find_all("div", {"class": "jobsearch-JobDescriptionSection-sectionItem"})
    salary_info_children = list(job_details_tree[0].children)
    salary = salary_info_children[1].text

    job_type_children = list(job_details_tree[1].children)
    job_type = job_type_children[1].text
except Exception:
    print("i fucked up")

# Qualfication section
# Not all jobs use this section
# qualification_tree = soup.find("div", {"id": "qualificationsSection"})
# if qualification_tree:
#     qualification_list = list(qualification_tree.children)[1]


# Job description section
job_description_tree = soup.find("div", {"id": "jobDescriptionText"})

def leaf_node_text(node):
    text = []

    def get_leaf_text(node):
        if isinstance(node, NavigableString):
            text.append(node)
            return

        children_list = list(node.children)
        for child_node in children_list:
            get_leaf_text(child_node)

    get_leaf_text(node)
    return text


def michelles_crappy_version(node):
    text = []
    all = node.find_all(string=True)


text = leaf_node_text(job_description_tree)
text_v2 = job_description_tree.find_all(string=True)


assert text == text_v2

# Footer metadata section
footer_tree = soup.find("div", {"class": "jobsearch-JobMetadataFooter"})
footer_tree_children = list(footer_tree.children)


days_posted = None
for child in footer_tree_children:
    if "days" in child.text:
        days_posted = child.text
        break


print(f"{title=} {company=} {salary=} {job_type=} {days_posted=}")
print(text)


result = {
    "title": title,
    "company": company,
    "salary": salary,
    "jobType": job_type,
    "dayPosted": days_posted,
    "jobDescription": text_v2
}

dumped = json.dumps(result)
pass