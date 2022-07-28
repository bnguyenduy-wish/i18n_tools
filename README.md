# i18n_tools

## Run

```
python gen_i18n_code.py file1.text file2.text ...
```

Output files are generated in the same folder: file1.py, file2.py, ...

## Input file example


```
subject | Spin to win special "deals", [[name]] 💰 ‘♞’
subject1 | Score daily discounts with the Blitz Buy wheel

header | Meet your wheel of deals, [[name]]
body | Spin the Blitz Buy wheel to unlock your number of daily deals

off_percent | 20% off
discount_banner_body | Enjoy [[off_percent]] your first order with code:
discount_banner_body2 | *Expires [[date]]. Max discount [[discount]]. In-app only.
discount_banner_body3 | Valid once.

```

## Output file example

```
from sweeper.i18n import i18n, ci18n

i18n_dict = {
    'subject': lambda name: i18n(u"Spin to win special \"deals\", {%1=name} \U0001f4b0 \u2018\u265e\u2019", name),
    'subject1': lambda: i18n(u"Score daily discounts with the Blitz Buy wheel"),
    'header': lambda name: i18n(u"Meet your wheel of deals, {%1=name}", name),
    'body': lambda: i18n(u"Spin the Blitz Buy wheel to unlock your number of daily deals"),
    'off_percent': lambda: i18n(u"20% off"),
    'discount_banner_body': lambda off_percent: i18n(u"Enjoy {%1=off_percent} your first order with code:", off_percent),
    'discount_banner_body2': lambda date, discount: i18n(u"*Expires {%1=date}. Max discount {%2=discount}. In-app only.", date, discount),
    'discount_banner_body3': lambda: i18n(u"Valid once."),
}
```

