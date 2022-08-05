# i18n_tools

## Run

```
python gen_i18n_code.py file1.text file2.text ...
```

Output files are generated in the same folder: file1.py, file2.py, ...

## Input file example

Normal sentence

```
string name | Sentence to translate
```

With context
```
string name | context: Context is here | Content is here
```

With variables
```
string name | Welcome { user name }, have a nice day!
```

Content can include non-unicode characters, emojis 

```
string name | Any content 🎉

```

Example input file

```
subject | Spin to win special "deals", {user name} ‘💰’
subject1 | Score daily discounts with the Blitz Buy wheel

header | Meet your wheel of deals, {user name}
body | Spin the Blitz Buy wheel to unlock your number of daily deals

off percent | context: Off percent of discount | {percent} off
discount banner body | Enjoy {off percent} your first order with code:
discount banner body2 | *Expires {date}. Max discount {discount amount}. In-app only.
discount banner body3 | context:  Discount code is only valid once. | Valid once.

```

## Output file example

```
from sweeper.i18n import i18n, ci18n

i18n_dict = {
    'subject': lambda user_name: i18n(u"Spin to win special \"deals\", {%1=user_name} \u2018\U0001f4b0\u2019", user_name),
    'subject1': lambda: i18n(u"Score daily discounts with the Blitz Buy wheel"),
    'header': lambda user_name: i18n(u"Meet your wheel of deals, {%1=user_name}", user_name),
    'body': lambda: i18n(u"Spin the Blitz Buy wheel to unlock your number of daily deals"),
    'off_percent': lambda percent: ci18n("Off percent of discount", u"{%1=percent} off", percent),
    'discount_banner_body': lambda off_percent: i18n(u"Enjoy {%1=off_percent} your first order with code:", off_percent),
    'discount_banner_body2': lambda date, discount_amount: i18n(u"*Expires {%1=date}. Max discount {%2=discount_amount}. In-app only.", date, discount_amount),
    'discount_banner_body3': lambda: ci18n("Discount code is only valid once.", u"Valid once."),
}
```

