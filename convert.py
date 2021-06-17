import cv2
import os
fps = 1
lists=[]
for i in os.listdir('./test_public'):
  lists.append(i)
os.mkdir('./videos')
for i in range(len(lists)):
  images=[]
  for item in os.listdir('./test_public/'+lists[i]):
    if(item.split('.')[1]=='jpg'):
      images.append('./test_public/'+lists[i]+'/'+item)
  img_tmp = cv2.imread(images[0])
  wp=img_tmp.shape
  fourcc = cv2.VideoWriter_fourcc(*'XVID')
  video_writer = cv2.VideoWriter(filename='./videos/'+lists[i]+'.avi', fourcc=fourcc, fps=fps, frameSize=(wp[1], wp[0]))  # 图片实际尺寸，不然生成的视频会打不开
  for j in range(len(images)):
    if os.path.exists(images[j]):  #判断图片是否存在
      img = cv2.imread(images[j])
      video_writer.write(img)
  video_writer.release()