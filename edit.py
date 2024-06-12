#-- DEPENDANCES --

from PIL import Image as pilp
from pathlib import Path

#-- EDITORS --

##edit/model/paint/class
class edit_model_paint:
	
	models={}
	
	def __init__(self,f_EditFunctions,f_Texts,f_Arguments=[]):
		#f_Texts : (<f_TextKey>,{f_TextAction},{f_TextHelp})
		#f_Argument[n] : (<f_Default>,{f_Name},{f_Type},{f_Min},{f_Max})
		self.m_editor=f_EditFunctions
		
		f_TextAction=None
		f_TextHelp=None
		if (type(f_Texts)==tuple):
			f_TextKey=f_Texts[0]
			if len(f_Texts)>1:
				f_TextAction=f_Texts[1]
			if len(f_Texts)>2:
				f_TextHelp=f_Texts[2]
		else:
			f_TextKey=f_Texts
		
		edit_model_paint.models[f_TextKey]=self
		self.m_text=f_TextAction if (f_TextAction!=None) else f_TextKey
		self.m_lore=f_TextHelp if (f_TextHelp!=None) else self.m_text

		self.m_rarg=[]
		n=0
		for v in f_Arguments:
			n+=1
			h_Name=f"arg {n}"
			h_Type=None
			h_Min=None
			h_Max=None
			if (type(v)==tuple):
				h_DefaultRequired=v[0]
				if (len(v)>1):
					h_Name=v[1]
				if (len(v)>2):
					h_Type=v[2]
				if (len(v)>3):
					h_Min=v[3]
				if (len(v)>4):
					h_Max=v[4]
			else:
				h_DefaultRequired=v
			
			self.m_rarg.append((h_DefaultRequired,h_Name,h_Type,h_Min,h_Max))

	
	def select(f_key):
		return edit_model_paint.models[f_key]
	def exist(f_key):
		return f_key in edit_model_paint.models
	def gef(self,f_mode=None):#getfunction
		if (type(self.m_editor)!=dict or f_mode==None):
			return self.m_editor
		else:
			return self.m_editor[f_mode]


##edit/tool/class
class edit_tool:
	def __init__(self,f_model_paint,f_paint_arg,f_select_id=None):
		self.painter=f_model_paint
		self.painter_arg=f_paint_arg#tulpe


#-- MODELS/PAINT --
#you can add your own models here
#paint is the action made to the pixel

##edit/model/paint/members
#edit_model_paint(<f_EditFunctions>,<f_TextKey>,<f_TextAction>)
#	f_EditFunctions : function OR dictionnary[<Mode:string>] function
#		the function / lambda editing the pixel
#	f_TextKey : string
#		key to use the command
#	f_TextAction : 

#make/negative
def make_pixel_neg_3(f_pix, f_arg):
	return tuple(255-f_pix[i] for i in range(3))
def make_pixel_neg_4(f_pix, f_arg):
	r=[255-f_pix[i] for i in range(3)]
	r.append(f_pix[3])
	return tuple(r)
edit_model_paint({"RGB":make_pixel_neg_3,"RGBA":make_pixel_neg_4}, ("neg", "négatif"))

#make/seil
#f_arg[0] : seil
def make_pixel_seuil(f_pix, f_arg):
	r_pix=[]
	for i in range(0,len(f_pix)):
		if (f_pix[i]>f_arg[0]):
			r_pix.append(255)
		else:
			r_pix.append(0)
	return tuple(r_pix)
edit_model_paint(make_pixel_seuil, ("seuil", "seuiller"), [(True,"valeur du seuil",int,0,255)])

#make/light
def make_pixel_dark_3(f_pix,f_arg):
	r_pix=[]
	for i in range(3):
		r_pix.append(f_pix[i]//f_arg)
	return tuple(r_pix)
def make_pixel_dark_4(f_pix,f_arg):
	r_pix=[]
	for i in range(3):
		r_pix.append(f_pix[i]//f_arg)
	r_pix.append(f_pix[3])
	return tuple(r_pix)
edit_model_paint({"RGB":make_pixel_dark_3,"RGBA":make_pixel_dark_4}, ("dark", "assombrir"))

def make_pixel_light_3(f_pix,f_arg):
	r_pix=[]
	for i in range(3):
		r_pix.append(255-((255-f_pix[i])//f_arg))
	return tuple(r_pix)
def make_pixel_light_4(f_pix,f_arg):
	r_pix=[]
	for i in range(3):
		r_pix.append(255-((255-f_pix[i])//f_arg))
	return tuple(r_pix)
edit_model_paint({"RGB":make_pixel_light_3,"RGBA":make_pixel_light_4}, ("light", "éclairer"))

#make/filters
def make_pixel_gray_3(f_pix,f_arg):
	h_lum=0
	for i in range(3):
		h_lum+=f_pix[i]
	h_lum//=3
	return(h_lum,h_lum,h_lum)
def make_pixel_gray_4(f_pix,f_arg):
	h_lum=0
	for i in range(3):
		h_lum+=f_pix[i]
	h_lum//=3
	return(h_lum,h_lum,h_lum,f_pix[3])
edit_model_paint({"RGB":make_pixel_gray_3,"RGBA":make_pixel_gray_4}, ("gray", "griser"))

def make_pixel_red_3(f_pix,f_arg):
	return(f_pix[0],0,0)
def make_pixel_red_4(f_pix,f_arg):
	return(f_pix[0],0,0,f_pix[3])
edit_model_paint({"RGB":make_pixel_red_3,"RGBA":make_pixel_red_4}, ("red", "filtre rouge"))
def make_pixel_green_3(f_pix,f_arg):
	return(0,f_pix[1],0)
def make_pixel_green_4(f_pix,f_arg):
	return(0,f_pix[1],0,f_pix[3])
edit_model_paint({"RGB":make_pixel_green_3,"RGBA":make_pixel_green_4}, ("red", "filtre vert"))
def make_pixel_blue_3(f_pix,f_arg):
	return(0,0,f_pix[2])
def make_pixel_blue_4(f_pix,f_arg):
	return(0,0,f_pix[2],f_pix[3])
edit_model_paint({"RGB":make_pixel_blue_3,"RGBA":make_pixel_blue_4}, ("red", "filtre bleu"))

#make/intresting
def make_pixel_lumin(f_pix,f_arg):
	r_pix=[]
	h_lum=0
	for i in range(3):
		h_lum+=f_pix[i]
	return (f_arg[0][h_lum*len(f_arg[0])//765])
edit_model_paint(make_pixel_lumin, ("lumin", "coloration par luminositée"), [(True,"liste des couleurs (tulpe) dans l'odre de luminosité" ,list)])

def make_pixel_rotate(f_pix):
	return(f_pix[2],f_pix[0],f_pix[1])

edit_model_paint(make_pixel_rotate, ("rotate", "rotation", "rotation des couleurs (de RGB vers BRG)"))



##edit/model/select/members


#-- IMAGE EDIT --

#main function
def edit_image_pixels(f_img, f_tool):
	
	h_editor=f_tool.painter.gef(f_img.mode)
	h_editor_arg=f_tool.painter_arg

	#select
	max_x=f_img.width
	max_y=f_img.height
	
	##keep trans
	#if (len(h_editor(f_img.getpixel((0,0)),h_editor_arg))==3 and len(f_img.getpixel((0,0)))==4):
	#	h_editor= lambda pix,arg : tuple(list(f_tool.painter.m_edit(pix,arg),pix[3]))
	
	for x in range(max_x):
		for y in range(max_y):
			f_img.putpixel((x,y),h_editor(f_img.getpixel((x,y)),h_editor_arg))#dirrectly put the pixel

#-- SELECTIONS --

	#for x in range(max_x//4,max_x//4*3):
	#	for y in range(max_y//4,max_y//4*3):

			#if ((x<max_x//4 or x>max_x*3//4) or (y<max_y//4 or y>max_y*3//4)):
			
	#c_x=f_img.width/2
	#c_y=f_img.height/2
	#r=((f_img.height**2+f_img.width**2)**(1/2))/4
			#if (((x-c_x)**2+(y-c_y)**2)<r**2):

	#c_x=f_img.width/2
	#c_y=f_img.height/2
	#r_x=(f_img.width)/4
	#r_y=(f_img.height)/4
			#if (((x-c_x)**2/r_x**2)+((y-c_y)**2/r_y**2)<1):


#-- SEI --

#@staticclass
class sei:

	##sei/settings
	allow_extentions=["png","jpg","jpeg","jpe","jfif","exif","webp"]
	
	##sei/say
	if_say={"info":True,"process":True,"in":True,"out":True,"warn":True,"error":True}
	if_rase=False
	__process=0

	def mute(f_IfMuted=True):
		f_IfMuted=not f_IfMuted
		for k in sei.if_say:
			sei.if_say[k]=f_IfMuted

	def say(f_text,f_type="info",f_bold=False):
		if (sei.if_say[f_type] and f_text!=None):
			h_fix=f"{f_type.upper()} : " if (f_bold) else ""
			h_tab=""
			for i in range(sei.__process):
				h_tab+="\t"
			print(f"{h_tab}{h_fix}{f_text}") 
	def say_in(f_text=None):
		sei.say(f_text,"in")
		sei.__process+=1
	def say_out(f_text=None):
		sei.__process-=1
		sei.say(f_text,"out")
	def say_error(f_text,f_exception=Exception):
		if (sei.if_rase):
			raise f_exception(f_text)
		else:
			sei.say(f_text,"error",True)
		return sei.if_rase
	
	##sei/say/help
	def help(*f_HelpSubcommands):
		print("no")



	##sei/folders
	folder_source=Path(__file__).parent.absolute()
	folder_save=Path(__file__).parent.absolute()

	def folder_check():
		sei.say_in("check if folders fine...")
		if (not Path.is_dir(sei.folder_source)):
			sei.say_error(f"check : [folder_source] not found ! ({sei.folder_source})",FileNotFoundError)
		elif (not Path.is_dir(sei.folder_save)):
			sei.say_error(f"check : [folder_save] not found ! ({sei.folder_save})",FileNotFoundError)
		else:
			sei.say_out("fine")
			return True
		sei.say_out()
		return False
	
	##sei/selection
	selection=[]
	images={}

	##sei/selection/select
	def p_select(f_ImageName):#private
		sei.selection.append(f_ImageName)

	#def select(f_ImageName=None,f_Extention="*",f_IsRecursive=True):
	#	if (f_ImageName==None):
	#		select_all(f_ImageName)
	#	else:
	#		select_one(f_ImageName)
	
	def select_one(f_ImageName):
		if (not Path.is_file(sei.folder_source.joinpath(f_ImageName))):
			sei.say_error(f"image to select not found ! ({f_ImageName})",FileNotFoundError)
		if (not Path(f_ImageName).suffix[1:] in sei.allow_extentions):
			sei.say_error(f"invalid file type ! ({f_ImageName})")
		sei.say(f"selecting [{f_ImageName}]","process")
		sei.p_select(f_ImageName)
		return True

	def select_all(f_FolderName="",f_Extention="*",f_IsRecursive=True):
		h_src=sei.folder_source.joinpath(f_FolderName)
		if (not Path.is_dir(h_src)):
			sei.say_error(f"invalid path ! ({h_src})",FileNotFoundError)
		if (f_IsRecursive):
			h_star="**/*"
		else:
			h_star="*"
		if (f_Extention=="*"):
			f_Extention=sei.allow_extentions
		else:
			if (type(f_Extention)!=list):
				f_Extention=[f_Extention]
			f_Extention=[f_Extention[i] for i in range(len(f_Extention)) if f_Extention[i] in sei.allow_extentions]
		h_elements=[]
		for v in f_Extention:
			h_glob=sorted(h_src.glob(f"{h_star}.{v}"))
			for v in h_glob:#you can make that in python
				h_elements.append(v.relative_to(sei.folder_source))
		sei.say_in(f"selecting {len(h_elements)} images")

		done=0
		for v in h_elements:
			if (not Path.is_file(sei.folder_source.joinpath(v))):
				sei.say_error(f"image to select not exist ! ({v})",FileNotFoundError)
			else:
				sei.p_select(v)
				done+=1

		sei.say_out(f"{done} images selected")
		
	def unselect_one(f_SelectedImageName):
		if (not f_SelectedImageName in sei.selection):
			sei.say_error(f"already not selected ({f_SelectedImageName})")
			return False
		sei.say(f"unselecting [{f_SelectedImageName}]","process")
		sei.selection.remove(f_SelectedImageName)
		return True
		
	def unselect_all():
		sei.say_in(f"unselecting {len(sei.selection)} images...")
		sei.selection.clear()
		sei.say_out(f"done")
		return True

	##sei/selection/open
	open_mode="RGBA"

	def p_open(f_SelectedImageName):
		sei.images[f_SelectedImageName]=pilp.open(sei.folder_source.joinpath(f_SelectedImageName)).convert(sei.open_mode)
		sei.selection.remove(f_SelectedImageName)

	def open_one(f_SelectedImageName):
		if (not f_SelectedImageName in sei.selection):
			sei.say_error(f"image not selected ({f_SelectedImageName})")
			return False
		sei.say(f"opening [{f_SelectedImageName}]")
		sei.p_open(f_SelectedImageName)
		return True

	def open_all():
		sei.say(f"opening {len(sei.selection)} images...")
		while (len(sei.selection)>0):
			sei.p_open(sei.selection[len(sei.selection)-1])
		sei.say("done")
		
	##sei/selection/select/close
	def p_close(f_OpenedImageName):
		del sei.images[f_OpenedImageName]

	def close_one(f_OpenedImageName):
		if (not f_OpenedImageName in sei.images):
			sei.say_error(f"image not opened ({f_OpenedImageName})")
			return False
		sei.say(f"closing [{f_OpenedImageName}]","process")
		sei.p_close(f_OpenedImageName)
		return True

	def close_all():
		sei.say(f"closing {len(sei.images)} images")
		#for k in sei.images.keys():
		#	sei.p_close(k)
		sei.images={}

	##sei/edit
	edit_tools=[]
	def tool_add(f_ToolId,f_ToolArguments=()):
		if (not edit_model_paint.exist(f_ToolId)):
			sei.say_error(f"wrong tool id. ({f_ToolId})",ValueError)
		h_ModelPaint=edit_model_paint.select(f_ToolId)
		if (type(f_ToolArguments)!=tuple):
			f_ToolArguments=(f_ToolArguments,)
		for i in range(len(h_ModelPaint.m_rarg)):
			h_rarg=h_ModelPaint.m_rarg[i]
			if (len(f_ToolArguments)<=i):
				sei.say_error(f"argument {i+1} for painter [{h_ModelPaint.m_text}] : not provided",ValueError)
			else:
				h_arg=f_ToolArguments[i]
				if (type(h_arg)!=h_ModelPaint.m_rarg[i][2]):
					sei.say_error(f"argument {i+1} for painter [{h_ModelPaint.m_text}] : of type {type(h_arg)} but expected type {h_ModelPaint.m_rarg[i][2]}",ValueError)
				elif (h_ModelPaint.m_rarg[i][3]!=None and h_arg<h_ModelPaint.m_rarg[i][3]):
					sei.say_error(f"argument {i+1} for painter [{h_ModelPaint.m_text}] : {h_arg} is not more than {h_ModelPaint.m_rarg[i][3]}",ValueError)
				elif (h_ModelPaint.m_rarg[i][4]!=None and h_arg>h_ModelPaint.m_rarg[i][4]):
					sei.say_error(f"argument {i+1} for painter [{h_ModelPaint.m_text}] : {h_arg} is not less than {h_ModelPaint.m_rarg[i][4]}",ValueError)
		for i in range(len(h_ModelPaint.m_rarg),len(f_ToolArguments)):
			sei.say_error(f"argument {i+1} for painter [{h_ModelPaint.m_text}] : provided but not expected ({f_ToolArguments[i]})",ValueError)
		print(f"range {len(h_ModelPaint.m_rarg)}")
		sei.edit_tools.append(edit_tool(h_ModelPaint,f_ToolArguments))

	def edit_pixels():
		sei.say_in(f"editing {len(sei.images)} images...")
		x=0
		for k in sei.images:
			x+=1
			#sei.say(f"({x}/{len(sei.images)})")
			y=0
			sei.say_in(f"[{k}] ({x}/{len(sei.images)})")
			for tool in sei.edit_tools:
				y+=1
				#sei.say(f"[{k}] ({x}/{len(sei.images)}) / {tool.painter.m_text} ({y}/{len(sei.edit_tools)})")
				sei.say(f"{tool.painter.m_text} ({y}/{len(sei.edit_tools)})")
				edit_image_pixels(sei.images[k],tool)
			sei.say_out()
		sei.say_out("done")	


	##sei/outpout
	def show():
		sei.say(f"showing {len(sei.images)} images...")
		for k in sei.images:
			sei.images[k].show()
		sei.say("done")

	def save(f_CloseAfter=True):
		sei.say(f"saving {len(sei.images)} images...")
		for k in sei.images:
			Path.mkdir(sei.folder_save.joinpath(k).parent,parents=True, exist_ok=True)
			sei.images[k].save(sei.folder_save.joinpath(k))
		if (f_CloseAfter):
			sei.close_all()
		sei.say("done")


#-- DOCUMENTATION --

##documentations/operations

#SEI : stand for SupraEdit Interface
	
	#sei.if_say= <IfSayWhatTheyDo:bool=True> : if program says the operations that do (what they do)
	#sei.mute(<IfMuted:bool=True>) : mute/unmute all messages
	#sei.if_rase= <IfRaseWhenError:bool=True> : if program rase when having not fatal trouble (however, they never raise when warn)

	#sei.folder_source= <SourceFolder:Path=Path(__file__).parent.absolute()> : the folder where images are
	#sei.folder_save= <SaveFolder:Path=Path(__file__).parent.absolute()> : the folder where you want save your creations
	#sei.folder_check= check if folders are well
	
	#sei.select_one( <ImageName> ) : load and select an image from the [folder_source]. can be in a subfolder.
	#sei.select_all( <f_FolderName:Path="">, <f_Extention:string="*">, <f_IsRecursive:bool=True> ) : load and select all images from the [folder_source].
	#sei.unselect_all() : unselect all selected images.
	#sei.open_mode= <OpenMode:text="RGB"> : the open mode.
	#sei.open_one( <SelectedImageName> ) : open a selected image.
	#sei.open_all() : open selected images.
	#sei.close_one( <OpenedImageName> ) : close an opened image.
	#sei.close_all() : close opened images.

	#sei.tool_add(<ToolId>,<ToolArguments=()>,<SelectorId>="all",<SelectorArguments=()>) : add a tool for a future edit. TODO : SELECTOR
	#sei.edit_pixels() : edit opened images using by-pixel operations. TODO

	#sei.show() : show all images with all changes.
	#sei.save() : save all images with all changes in the [folder_save]. TODO