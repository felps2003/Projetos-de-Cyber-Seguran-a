import torch
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image, ImageOps
from captcha.image import ImageCaptcha
import cv2
from google.colab.patches import cv2_imshow
import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog
from PIL import Image, ImageOps


#Função de teste: Essa função contem a IA do Detectron2, que verifica se 
#a imagem atende aos requisitos, e gera uma lista com oque achou.
def teste(image):
  image = cv2.imread(image)
  cfg = get_cfg()
  cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_X_101_32x8d_FPN_3x.yaml"))
  cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/faster_rcnn_X_101_32x8d_FPN_3x.yaml")
  cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.6
  predictor = DefaultPredictor(cfg)
  outputs = predictor(image)
  outputs["instances"].pred_classes
  outputs["instances"].pred_boxes
  achados = []
  for data in outputs["instances"].pred_classes:
    num = data.item()
    lista = (MetadataCatalog.get(cfg.DATASETS.TRAIN[0]).thing_classes[num])
    if 'person' in lista:
      x = lista
      achados.append(x)
    if 'apple' in lista:
      x = lista
      achados.append(x)
    if 'clock' in lista:
      x = lista
      achados.append(x)
    if 'pen' in lista:
      x = lista
      achados.append(x)
  return achados


def predImage(image):
  image = cv2.imread(image)
  cfg = get_cfg()
  cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_X_101_32x8d_FPN_3x.yaml"))
  cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/faster_rcnn_X_101_32x8d_FPN_3x.yaml")
  cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.6
  predictor = DefaultPredictor(cfg)
  outputs = predictor(image)
  outputs["instances"].pred_classes
  outputs["instances"].pred_boxes
  viz = Visualizer(image[:,:,::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN[0]))
  outputs = viz.draw_instance_predictions(outputs["instances"].to("cpu"))
  filename = 'result.jpg'
  cv2.imwrite(filename, outputs.get_image()[:,:,::-1])
  cv2.waitKey(0)
  cv2.destroyAllWindows()
  


#Função de Criação do Captcha: Essa função cria o captcha de forma aleatoria.
def criandoCaptcha():
  captcha_text = '12teste'
  image_info = ImageCaptcha(width=250, height=100)
  source = image_info.generate(captcha_text)
  image_info.write(captcha_text, 'Captcha.png')
  imagemCaptcha = cv2.imread("./Captcha.png")
  return imagemCaptcha



#Função de teste do Captcha: Essa função testa se o usuario escreveu de forma
#correta o que está escrito na imagem do Captcha.
def captchaTeste(item):
  captcha_text = '12teste'
  if item == captcha_text:
    st.success("Parabéns o Captcha está certo")
    return True
  elif item != captcha_text:
    st.warning("Digite o Captcha")
    return False



st.set_page_config(layout="centered", page_icon="💬", page_title="Banco com defesa de IA")
st.title("💬 Banco com defesa de IA")
st.markdown(
  "#### Para realização do seu cadastro no nosso APP, porfavor passe por essas seguranças"
)
esquerda, direita = st.columns(2)
# formulario esquerda
formEsq = esquerda.form("template_formEsq")
formEsq.markdown("### Captcha")
botaoCap = formEsq.form_submit_button("Clique aqui para ver o captcha")
if botaoCap:
  formEsq.image(criandoCaptcha(), caption = '',use_column_width='always')

# formulario direita
formDir = direita.form("template_formDir")
formDir.markdown("### Digite aqui")
escrita = formDir.text_input('')
botaoVer = formDir.form_submit_button("Verificar")
formDir.markdown("")
formDir.markdown("")
x = captchaTeste(escrita)
if x == True:
  st.markdown("#### Por favor, faça upload de uma self menor que (7kb)")
  st.write("Criterios: Ter duas pessoas na self ou Self segurando uma (maçã,caneta ou um relogio)")
  imagem = st.file_uploader("", type=['png','jpeg','jpg'])
  ladoEsq, meio ,ladoDir = st.columns(3)
  if imagem is not None:
    img = Image.open(imagem)
    ladoEsq.image(img)
    with open(imagem.name, mode = "wb") as f:
      f.write(imagem.getbuffer())
    predImage(imagem.name)
  verificar = meio.button("Verificar a self escolhida")
  if verificar:
    img_ = Image.open("result.jpg")
    ladoDir.image(img_)
    try:
      lista = teste(imagem.name)
      if ('person' in lista and 'apple' in lista) or ('person' in lista and 'clock' in lista) or ('person' in lista and 'pen' in lista) or (lista.count('person') >= 2):
        meio.success("🎉 Parabéns você tem permissão de fazer o cadastro")
        st.balloons()
      else:
        meio.error("Infelizmente não foi permitido realizar o cadastro")
        meio.error("Por favor faça a self novamente, mas seguindo os criterios")
    except:
      st.warning("Por favor, faça upload da sua self")