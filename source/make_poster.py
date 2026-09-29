from PIL import Image, ImageDraw, ImageFont, ImageFilter
import sys
SRC=r"D:\SteamLibrary\steamapps\workshop\content\108600\3785397275\mods\ExtractionMode\poster.png"
BLUE=(0,35,149); WHITE=(245,245,245); RED=(237,41,57)
def make(out, dist=118, width=74):
    base=Image.open(SRC).convert("RGBA"); W,H=base.size
    S=4  # suréchantillonnage
    L=int(W*1.6)
    band=Image.new("RGBA",(L*S,width*S),(0,0,0,0)); d=ImageDraw.Draw(band)
    e=width*S//5
    d.rectangle([0,0,L*S,e],fill=BLUE); d.rectangle([0,e,L*S,width*S-e],fill=WHITE); d.rectangle([0,width*S-e,L*S,width*S],fill=RED)
    f=ImageFont.truetype(r"C:\Windows\Fonts\impact.ttf",int(width*0.5)*S)
    t="TRADUCTION FR"; bb=d.textbbox((0,0),t,font=f)
    tw,th=bb[2]-bb[0],bb[3]-bb[1]
    d.text(((L*S-tw)//2-bb[0],(width*S-th)//2-bb[1]),t,font=f,fill=(20,24,40))
    band=band.resize((L,width),Image.LANCZOS).rotate(-45,expand=True,resample=Image.BICUBIC)
    # ombre
    sh=Image.new("RGBA",band.size,(0,0,0,0)); sh.putalpha(band.getchannel("A").point(lambda a:int(a*0.6)))
    sh=sh.filter(ImageFilter.GaussianBlur(6))
    # centre du bandeau à distance `dist` du coin haut-droit, le long de la diagonale
    import math
    cx=W-dist/math.sqrt(2); cy=dist/math.sqrt(2)
    pos=(int(cx-band.width/2),int(cy-band.height/2))
    layer=Image.new("RGBA",base.size,(0,0,0,0))
    layer.alpha_composite(sh,(pos[0]+3,pos[1]+5)) if pos[0]+3>=0 else None
    tmp=Image.new("RGBA",base.size,(0,0,0,0)); tmp.paste(sh,(pos[0]+3,pos[1]+5),sh)
    base=Image.alpha_composite(base,tmp)
    tmp=Image.new("RGBA",base.size,(0,0,0,0)); tmp.paste(band,pos,band)
    base=Image.alpha_composite(base,tmp)
    base.convert("RGB").save(out)
make(sys.argv[1] if len(sys.argv)>1 else "poster_fr.png")
