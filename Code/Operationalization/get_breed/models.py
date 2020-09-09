from django.db import models
import requests
import pandas as pd
import cv2
import urllib.request
import numpy as np
from matplotlib import pyplot as plt
from get_breed import globalTrainResults
img_h, img_w = 64, 64 # Altura e largura das imagens

# Create your models here.

class Pictures(models.Model):
    id=models.AutoField(primary_key=True)
    address =  models.CharField(max_length=200, blank=False, null=False)
    real_breed = models.CharField(max_length=50, blank=True)
    classification = models.CharField(max_length=50, blank=True)
    estimated_score1 = models.FloatField(null=True)
    estimated_score2 = models.FloatField(null=True)
    estimated_score3 = models.FloatField(null=True)

    # def __str__(self):
    #     return self.address

    def save_estimate(self):

        # Convert Images
        req = urllib.request.urlopen(self.address)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        img = cv2.imdecode(arr,0)
        imres = cv2.resize(img, (img_h, img_w), interpolation=cv2.INTER_CUBIC)
        photo = imres.flatten()
        # Get variables and model
        model = globalTrainResults
        #variables = globalTrainResults['variables']
        # Prepare data: must be in the same order as the model was trained
        photos = []
        photos.append(photo)

        # Use model to predict
        self.classification = model.predict(photos)[0]
        estimatives = model.predict_proba(photos)[0]
        self.estimated_score1 = estimatives[0]
        self.estimated_score2 = estimatives[1]
        self.estimated_score3 = estimatives[2]
#        self.estimated_score = model.predict_proba(photos)[0][0]
        self.save()

    class Meta:
        unique_together = ('address',)
