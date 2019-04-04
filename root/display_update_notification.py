from win10toast import ToastNotifier
from pathlib import Path
toaster = ToastNotifier()
path = Path.cwd()
toaster.show_toast("Transit Analyst Israel Update", "Transit Analyst Israel will be updated at 22:30."
                                                    " Please leave your machine on and plugged-in."
                                                    " Docker Desktop should be restarted and Navitia server running.",
                   icon_path= path.parent / "website_no_data" / "docs" / "images" / "favicon.ico",
                   duration="300")


