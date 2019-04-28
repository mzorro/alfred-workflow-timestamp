#!/usr/bin/python
# encoding: utf-8

import sys,time,re

# Workflow3 supports Alfred 3's new features. The `Workflow` class
# is also compatible with Alfred 2.
from workflow import Workflow3

ICON = 'icon.png'

def format(secs):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(secs))

def diff(sourceSecs, targetSecs, suffix='之后'):
    d = sourceSecs - targetSecs
    if d < 0: return diff(targetSecs, sourceSecs, '之前')
    s = d % 60
    d /= 60
    m = d % 60
    d /= 60
    h = d % 24
    d /= 24
    r = ''
    if d > 0: r += str(d) + '天'
    if h > 0: r += str(h) + '时'
    if m > 0: r += str(m) + '分'
    if s > 0 or not r: r += str(s) + '秒'
    return r + suffix

def main(wf):
    args = wf.args

    nowMills = int(time.time()*1000)
    nowSecs = nowMills/1000
    def now():
        wf.add_item(title=nowMills,
                    subtitle='现在的毫秒数',
                    arg=nowMills,
                    valid=True,
                    icon=ICON)
        wf.add_item(title=format(nowSecs),
                    subtitle='现在时间',
                    arg=format(nowSecs),
                    valid=True,
                    icon=ICON)

    if not args[0] or args[0] == 'now':
        now()
    elif args[0].isdigit():
        secs = int(args[0])/1000
        s = format(secs)
        wf.add_item(title=s,
                    subtitle=diff(secs, nowSecs),
                    arg=s,
                    valid=True,
                    icon=ICON)
    else:
        fa = ['%Y', '%m', '%d', '%H', '%M', '%S']
        prefix = ['', '-', '-', ' ', ':', ':']
        f = ''
        s = ''
        for (index, val) in enumerate(re.findall(r'\d+', args[0])):
            f += prefix[index] + fa[index]
            s += prefix[index] + val
        if f:
            secs = int(time.mktime(time.strptime(s, f)))
            mills = secs * 1000
            wf.add_item(title=mills,
                        subtitle=diff(secs, nowSecs),
                        arg=mills,
                        valid=True,
                        icon=ICON)
    wf.send_feedback()


if __name__ == '__main__':
    # Create a global `Workflow3` object
    wf = Workflow3()
    # Call your entry function via `Workflow3.run()` to enable its
    # helper functions, like exception catching, ARGV normalization,
    # magic arguments etc.
    sys.exit(wf.run(main))