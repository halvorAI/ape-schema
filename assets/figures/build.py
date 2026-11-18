# Builds hero-wide.svg and hero-narrow.svg. Run: python3 assets/figures/build.py
import sys, os
out = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
STYLE = """<style>
.bg{fill:#FBF9F4}.box{fill:#F3EFE6;stroke:#7A766C;stroke-width:1.5}.hb{fill:#F3EFE6;stroke:#4A6100;stroke-width:2.5}
.t{fill:#1C1C1C;font:600 16px 'IBM Plex Sans',system-ui,-apple-system,'Segoe UI',sans-serif}
.s{fill:#5F5B52;font:400 13px 'IBM Plex Sans',system-ui,-apple-system,'Segoe UI',sans-serif}
.k{fill:#5F5B52;font:600 11px 'IBM Plex Mono',ui-monospace,Menlo,monospace;letter-spacing:.08em}
.f{fill:#1C1C1C;font:400 14px 'IBM Plex Sans',system-ui,-apple-system,'Segoe UI',sans-serif}
.a{stroke:#1C1C1C;stroke-width:2;fill:none}.d{stroke:#4A6100;stroke-width:2;stroke-dasharray:6 5;fill:none}
.ah{fill:#1C1C1C}.dh{fill:#4A6100}.ok{fill:#4A6100;font:700 16px system-ui,sans-serif}.acc{fill:#4A6100}
@media (prefers-color-scheme:dark){.bg{fill:#1C1C1C}.box{fill:#262624;stroke:#7A766C}.hb{fill:#262624;stroke:#C6F432}
.t,.f{fill:#F3EFE6}.s,.k{fill:#A39E91}.a{stroke:#F3EFE6}.ah{fill:#F3EFE6}.d{stroke:#C6F432}.dh,.acc{fill:#C6F432}.ok{fill:#C6F432}}
</style>"""
def box(x,y,w,h,title,sub,cls="box",check=False):
    s=f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="10"/>'
    s+=f'<text class="t" x="{x+16}" y="{y+28}">{title}</text>'
    s+=f'<text class="s" x="{x+16}" y="{y+50}">{sub}</text>'
    if check: s+=f'<text class="ok" x="{x+w-30}" y="{y+29}">✓</text>'
    return s
def harrow(x1,x2,y,cls="a",head="ah"):
    return f'<line class="{cls}" x1="{x1}" y1="{y}" x2="{x2-9}" y2="{y}"/><path class="{head}" d="M{x2} {y} l-11 -6 v12z"/>'
def varrow(x,y1,y2,cls="a",head="ah"):
    return f'<line class="{cls}" x1="{x}" y1="{y1}" x2="{x}" y2="{y2-9}"/><path class="{head}" d="M{x} {y2} l-6 -11 h12z"/>'
ALT="An AI agent pays a merchant over a payment rail such as Stripe, a card, x402 or MPP. HalvorAI is not on that path. Beside it, the HalvorAI SDK observes the payment read-only and records a signed event, events are assembled into a signed evidence pack, and the bank verifies the pack offline."
def svg(w,h,body,title):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-labelledby="t d"><title id="t">{title}</title><desc id="d">{ALT}</desc>{STYLE}<rect class="bg" width="{w}" height="{h}" rx="14"/>{body}</svg>\n'
TITLE="HalvorAI records evidence beside the payment path"
# wide
W,H=960,360; bw,bh=256,66; xs=[40,352,664]
b='<text class="k" x="40" y="44">PAYMENT PATH</text>'
y1=60
b+=box(xs[0],y1,bw,bh,"AI agent","pays on an owner's behalf")
b+=box(xs[1],y1,bw,bh,"Payment rail","Stripe · card · x402 · MPP")
b+=box(xs[2],y1,bw,bh,"Merchant","gets paid, nothing added")
b+=harrow(xs[0]+bw+4,xs[1]-4,y1+bh/2)+harrow(xs[1]+bw+4,xs[2]-4,y1+bh/2)
y2=206
b+=f'<text class="k" x="40" y="{y2-16}">EVIDENCE, BESIDE THE PATH</text>'
b+=varrow(xs[0]+bw-36,y1+bh+4,y2-4,"d","dh")
b+=f'<text class="s" x="{xs[0]+bw-24}" y="{y1+bh+44}">observes, read-only</text>'
b+=box(xs[0],y2,bw,bh,"HalvorAI SDK","signs one event per payment","hb")
b+=box(xs[1],y2,bw,bh,"Evidence pack","signed manifest, hash chain")
b+=box(xs[2],y2,bw,bh,"Your bank","verifies offline, no trust in us",check=True)
b+=harrow(xs[0]+bw+4,xs[1]-4,y2+bh/2)+harrow(xs[1]+bw+4,xs[2]-4,y2+bh/2)
b+=f'<text class="f" x="40" y="{H-34}">HalvorAI is never in the payment path. It cannot slow or block a payment.</text>'
open(os.path.join(out,"hero-wide.svg"),"w").write(svg(W,H,b,TITLE))
# narrow
W,H=440,480; bw,bh=184,66; xl,xr=24,232; ys=[78,214,350]
b=f'<text class="k" x="{xl}" y="52">PAYMENT PATH</text><text class="k" x="{xr}" y="52">EVIDENCE</text>'
L=[("AI agent","pays for an owner"),("Payment rail","Stripe · card · x402"),("Merchant","gets paid")]
R=[("HalvorAI SDK","signs each event"),("Evidence pack","signed, hash-chained"),("Your bank","verifies offline")]
for i,y in enumerate(ys):
    b+=box(xl,y,bw,bh,*L[i])
    b+=box(xr,y,bw,bh,*R[i],cls="hb" if i==0 else "box",check=(i==2))
    if i<2:
        b+=varrow(xl+bw/2,y+bh+4,ys[i+1]-4)+varrow(xr+bw/2,y+bh+4,ys[i+1]-4)
b+=harrow(xl+bw+2,xr-2,ys[0]+bh/2,"d","dh")
b+=f'<text class="s" x="{xl}" y="{ys[2]+bh+40}">The SDK observes read-only. HalvorAI is never</text>'
b+=f'<text class="s" x="{xl}" y="{ys[2]+bh+60}">in the payment path and cannot slow or block it.</text>'
open(os.path.join(out,"hero-narrow.svg"),"w").write(svg(W,H,b,TITLE))
