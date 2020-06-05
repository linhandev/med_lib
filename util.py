from pypinyin import pinyin, Style


def to_pinyin(name, nonum=False):
    new_name = ""
    for ch in name:
        if u"\u4e00" <= ch <= u"\u9fff":
            new_name += pinyin(ch, style=Style.NORMAL)[0][0]
        else:
            if nonum and ("0" <= ch <= "9" or ch == "_"):
                continue
            new_name += ch
    return new_name
