from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse

from forecast.serializers import *
from forecast.models import *
import logging

import pandas as pd
from datetime import datetime, timedelta
import pickle

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
PROJECT_FOLDER = 'C:/Users/thewr/git/mit_data_science.git/'

def dashboard_home(requests):
    from forecast import dashboard
        
    dashboard.update_dash()
    return render(requests, 'index.html')


class MeasurementsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows measurements to be viewed or edited.
    """
    # queryset =
    serializer_class = MeasurementsSerializer
    queryset = Measurements.objects.all()
    
class ForecastModelsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ForecastModels to be viewed or edited.
    """
    queryset = ForecastModels.objects.all()
    serializer_class = ForecastModelsSerializer


class ForecastsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Forecasts to be viewed or edited.
    """
    queryset = Forecasts.objects.all()
    serializer_class = ForecastsSerializer

class UpdateModels(APIView):
  
  def get(self, request):
      try:
            # Read database from pipeline_training
            data_proc_file = PROJECT_FOLDER + '/Data/Processed/energy_consumption_data_modeling.parquet'
            data = pd.read_parquet(data_proc_file)
            data = data.copy()
            # Loop over forecast samples
            measurement_list = []
            for irow, row in data.iterrows():
                if not Measurements.objects.filter(date=row.Datetime).exists():
                    
                    measurement = Measurements(date=row.Datetime,                                         
                                                PJME_MW= row.PJME_MW)                                         
                    measurement_list.append(measurement)

            # Bulk insert
            if len(measurement_list):
                Measurements.objects.bulk_create(measurement_list)

            serial_data = MeasurementsSerializer(measurement_list,
                                             many=True,context={'request': request})   

            return Response(serial_data.data, status=status.HTTP_200_OK)

      except Exception as err:
        return Response('Detailed Error: ' + err.__str__(), status = status.HTTP_400_BAD_REQUEST)


class TrainModels(APIView):
  def get(self, request):
    try:
        # run training pipeline
        notebook_filename = PROJECT_FOLDER + '/Code/Operationalization/training/pipeline_training.ipynb'
        print(notebook_filename)
        with open(notebook_filename) as f:
            nb = nbformat.read(f, as_version=4)
        ep = ExecutePreprocessor(timeout=20000, kernel_name='python3')
        ep.preprocess(nb, {'metadata': {'path': PROJECT_FOLDER}})
        # Saved model and results
        model_score_file = PROJECT_FOLDER + '/Data/Modeling/model_scores.parquet'
        # load dataframe
        df_results = pd.read_parquet(model_score_file)
        print(df_results)
        # Create in memory objects
        object_list = []
        for i, row in df_results.iterrows():
            # Create the new forecast model
            
            if not ForecastModels.objects.filter(name = row.model_name,
                                                 train_last_date= row.date_end).exists():
                                                             
                forecast_model = ForecastModels(name = row.model_name,
                                                train_last_date= row.date_end,
                                                train_initial_date = row.date_begin,
                                                test_score=row.score)
                object_list.append(forecast_model)
                # Deactivate other models
                objs = ForecastModels.objects.filter(name=row.model_name)
                                         
                for obj in objs:
                    obj.status=False
                    obj.save()

        # Create the forecast model
        if len(object_list):
            ForecastModels.objects.bulk_create(object_list)        

        # Serialize the list of Forecast Models
        serial_data = ForecastModelsSerializer(ForecastModels.objects.filter(status=True),
                                               many=True,
                                               context={'request': request})

        return Response(serial_data.data, status=status.HTTP_200_OK)
        
    except Exception as err:
        return Response('Detailed Error: ' + err.__str__(), status = status.HTTP_400_BAD_REQUEST)

class ForecastEnergy(APIView):
  
  def get(self, request):
   
    try:
        forecasts_list = []
        model_name = request.query_params['model_name']

        # Get ForecastModel object
        forecastmodel = ForecastModels.objects.get(name=model_name,
                                                   #country=country,
                                                   status=True)
        # Load models
        model_score_file = PROJECT_FOLDER + '/Data/Modeling/model_scores.parquet'
        model_file = PROJECT_FOLDER + '/Data/Modeling/trained_models.jbl'
        data_proc_file = PROJECT_FOLDER + '/Data/Processed/energy_consumption_data_modeling.parquet'
        with open(model_file, 'rb') as fid:
            trained_models = pickle.load(fid)
        # Check country code
        
        model = trained_models
        # load dataframe
        df_results = pd.read_parquet(model_score_file)
        model_last_date = df_results.date_end.dt.date.values[0]
        # model_last_date = forecastmodel.train_last_date

        df_pjme = pd.read_parquet(data_proc_file)

        logging.info("predicao")

        # Evaluate Model     
        
        forecast_days = 5
        date_max = model_last_date + timedelta(forecast_days)
        n_periods = 24*forecast_days  

        logging.info('make future dataframe')       

        forecast_data = model.make_future_dataframe(
        periods=n_periods, freq='h',include_history=False)

        logging.info('vai fazer a predicao gerando df_forecast')  

        df_forecast= model.predict(forecast_data).rename(columns={'Datetime':'ds'})
        logging.info('predicao realizada')  
               
        logging.info('vai pegar  df_forecast como forecast e renomear yhat como forecast')

        forecast = df_forecast[['ds','yhat']].reset_index().rename(columns={'yhat':'forecast'})
        logging.info(forecast.info()) 
           
        
        logging.info('vai iterar por forecast e criar o ojb')

        # Save forecast objects
        for index, row in  forecast.iterrows():           
            logging.info('entrou no iteracao')
            if not Forecasts.objects.filter(date=row.ds).exists():
                logging.info('setando measurement')
               
                measurement = Measurements(date=row.ds,
                                                PJME_MW = 0.0)        

                logging.info('setando forecast')
                forecast = Forecasts(PJME_MW= row.forecast,
                                   date=row.ds,
                                   error = 0.0,
                                   forecast_model = forecastmodel,
                                   measurement = measurement)

                logging.info('inserindo forecast na lista')                                                                
                forecasts_list.append(forecast)
                logging.info('criou a lista de objetos forecast') 
              

        # Bulk insert
        if len(forecasts_list):
          Forecasts.objects.bulk_create(forecasts_list) 
          logging.info('vai retornar o response')          
                                           
        forecast_objs = [obj for obj in Forecasts.objects.filter(forecast_model=forecastmodel)
                         if obj.date >= forecastmodel.train_last_date]
        serial_data = ForecastsSerializer(forecast_objs,
                                           many=True,
                                           context={'request': request})

        return Response(serial_data.data, status=status.HTTP_200_OK)

    except Exception as err:
        return Response('Detailed Error: ' + err.__str__(), status = status.HTTP_400_BAD_REQUEST)

class ForecastEvaluation(APIView):
  
  def get(self, request):
   
    try:
        forecasts_list = []
        model_name = request.query_params['model_name']

        # Get ForecastModel object
        forecastmodel = ForecastModels.objects.get(name=model_name,
                                                   #country=country,
                                                   status=True)
        # Load models
        model_score_file = PROJECT_FOLDER + '/Data/Modeling/model_scores.parquet'
        model_file = PROJECT_FOLDER + '/Data/Modeling/trained_models.jbl'
        data_proc_file = PROJECT_FOLDER + '/Data/Processed/energy_consumption_data_modeling.parquet'
        with open(model_file, 'rb') as fid:
            trained_models = pickle.load(fid)
        # Check country code
        
        logging.info('vai iterar por forecast e criar o ojb')

          
        first_forecast  = Forecasts.objects.filter(measurement__isnull=True).first()
        forecast_model_evaluated = first_forecast.forecast_model
        forecasts_set = Forecasts.objects.filter(measurement__isnull=True) 
        if forecasts_set:
            for forecast in forecasts_set: 
                forecast_model = forecast.forecast_model               
                logging.info('pegou o forecast. Vai verificar se tem measurement no banco')
                if Measurements.objects.filter(date=forecast.date).exists() and Measurements.objects.filter(date=forecast.date).count() == 1:
                    forecast_measurement = Measurements.objects.get(date=forecast.date)
                    logging.info('Achou o measurement do forecast para editar')
                    logging.info('Editou o measurement do forecast')
                    forecast_error = forecast.PJME_MW - forecast_measurement.PJME_MW
                    percentage_error = (forecast_error / forecast_measurement.PJME_MW) * 100
                    logging.info('setou o measurement do forecast e salvou')
                    Forecasts.objects.filter(date=forecast.date).update(measurement = forecast_measurement, error=forecast_error, percentage_error=percentage_error)
       

        logging.info('terminou de atualizar os forecasts com os mearuments novos do banco.')
        forecasts_updated = Forecasts.objects.filter(forecast_model = forecast_model_evaluated)             
        serial_data = ForecastsSerializer(forecasts_updated,
                                           many=True,
                                           context={'request': request})

        return Response(serial_data.data,status=status.HTTP_200_OK)

    except Exception as err:
        return Response('Detailed Error: ' + err.__str__(), status = status.HTTP_400_BAD_REQUEST)