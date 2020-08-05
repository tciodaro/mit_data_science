
from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse

from forecast.serializers import *
from forecast.models import *

import pandas as pd
from datetime import datetime
import pickle

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
PROJECT_FOLDER = 'C:/Users/BZ241WX/Documents/InfNet/CursoPosDataScience/mit_data_science/'



class MeasurementsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows measurements to be viewed or edited.
    """
    # queryset =
    serializer_class = MeasurementsSerializer
    queryset = Measurements.objects.all()

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `countrycode` query parameter in the URL.
        """
        countrycode = self.request.query_params.get('countrycode', None)
        queryset = Measurements.objects.all()
        if countrycode is not None:
            if Countries.objects.filter(code=countrycode).exists():
                country = Countries.objects.get(code=countrycode)
                queryset = queryset.filter(country=country.id)

        return queryset


class CountriesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows countries to be viewed or edited.
    """
    queryset = Countries.objects.all()
    serializer_class = CountriesSerializer



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
  """
  """
  def _update_measurements(self):
      # Read database from pipeline_training
      data_proc_file = PROJECT_FOLDER + '/Data/Processed/covid19_data_modeling.parquet'
      data = pd.read_parquet(data_proc_file)
      # Filter for countries with models
      model_countries = [obj.country.code for obj in ForecastModels.objects.all()]
      data = data[data.countrycode.isin(model_countries)].copy()
      # Loop over forecast samples
      measurement_list = []
      for irow, row in data.iterrows():
          country = Countries.objects.get(code=row.countrycode)
          if not Measurements.objects.filter(date=row.date, country=country).exists():
              measurement = Measurements(date=row.date,
                                         country=country,
                                         cases = row.cases,
                                         deaths = row.deaths,
                                         recovered = row.recovered)
              measurement_list.append(measurement)

      # Bulk insert
      if len(measurement_list):
          Measurements.objects.bulk_create(measurement_list)


  def get(self, request):
    """
    """
    try:
        # run training pipeline
        notebook_filename = PROJECT_FOLDER + '/Code/Operationalization/pipeline_training.ipynb'
        print(notebook_filename)
        with open(notebook_filename) as f:
            nb = nbformat.read(f, as_version=4)
        ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
        ep.preprocess(nb, {'metadata': {'path': PROJECT_FOLDER}})
        # Saved model and results
        model_score_file = PROJECT_FOLDER + '/Data/Modeling/model_scores.parquet'
        # model_file = PROJECT_FOLDER + '/Data/Modeling/trained_models.jbl'
        # load dataframe
        df_results = pd.read_parquet(model_score_file)
        print(df_results)
        # Create in memory objects
        object_list = []
        for i, row in df_results.iterrows():
            # Get of create country
            country, flag = Countries.objects.get_or_create(code=row.countrycode)
            # Create the new forecast model
            # print(row)
            if not ForecastModels.objects.filter(name = row.model_name,
                                                 train_last_date= row.date_end,
                                                 country=country).exists():
                forecast_model = ForecastModels(name = row.model_name,
                                                train_last_date= row.date_end,
                                                country=country,
                                                test_score=row.score)
                object_list.append(forecast_model)
                # Deactivate other models for this country
                objs = ForecastModels.objects.filter(name=row.model_name,
                                                     country = country)
                for obj in objs:
                    obj.status=False
                    obj.save()

        # Create the forecast model
        if len(object_list):
            ForecastModels.objects.bulk_create(object_list)

        # Update measurements
        self._update_measurements()

        # Serialize the list of Forecast Models
        serial_data = ForecastModelsSerializer(ForecastModels.objects.filter(status=True),
                                               many=True,
                                               context={'request': request})

        return Response(serial_data.data, status=status.HTTP_200_OK)

    except Exception as err:
        return Response('Detailed Error: ' + err.__str__(), status = status.HTTP_400_BAD_REQUEST)






class ForecastCountry(APIView):
  """
  """
  def get(self, request):
    """
    Return the refurbishments
    """
    try:
        countrycode = request.query_params['countrycode']
        to_date = request.query_params['to_date']
        model_name = request.query_params['model_name']

        # Get ForecastModel object
        date_max = datetime.strptime(to_date, '%Y-%m-%d').date()
        country = Countries.objects.get(code=countrycode)
        forecastmodel = ForecastModels.objects.get(name=model_name,
                                                   country=country,
                                                   status=True)
        # Load models
        model_score_file = PROJECT_FOLDER + '/Data/Modeling/model_scores.parquet'
        model_file = PROJECT_FOLDER + '/Data/Modeling/trained_models.jbl'
        with open(model_file, 'rb') as fid:
            trained_models = pickle.load(fid)
        # Check country code
        if countrycode not in trained_models.keys():
            return Response('could not find country ' + countrycode, status = status.HTTP_400_BAD_REQUEST)

        model = trained_models[countrycode]
        # load dataframe
        df_results = pd.read_parquet(model_score_file)
        model_last_date = df_results[df_results.countrycode==countrycode].date_end.dt.date.values[0]
        # model_last_date = forecastmodel.train_last_date

        # Evaluate Model
        n_periods = (date_max - model_last_date).days
        forecast_data = model.make_future_dataframe(
            periods=n_periods,
            include_history=True
            )
        df_forecast = model.predict(forecast_data).set_index('ds')
        forecast     = df_forecast.yhat[-n_periods:].rename('forecast')

        # Save forecast objects
        for dt, estimate in forecast.iteritems():
            obj,flag = Forecasts.objects.get_or_create(date=dt,
                                                       forecast_model=forecastmodel)
            obj.estimated_cases=estimate
            obj.save()

        forecast_objs = [obj for obj in Forecasts.objects.filter(forecast_model=forecastmodel)
                         if obj.date >= forecastmodel.train_last_date]
        serial_data = ForecastsSerializer(forecast_objs,
                                           many=True,
                                           context={'request': request})

        return Response(serial_data.data, status=status.HTTP_200_OK)

    except Exception as err:
        return Response('Detailed Error: ' + err.__str__(), status = status.HTTP_400_BAD_REQUEST)
