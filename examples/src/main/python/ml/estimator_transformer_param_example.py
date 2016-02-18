#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
Estimator Transformer Param Example.
"""
from pyspark import SparkContext, SQLContext
from pyspark.mllib.linalg import Vectors
# $example on$
from pyspark.ml.classification import LogisticRegression
# $example off$

if __name__ == "__main__":

    sc = SparkContext(appName="EstimatorTransformerParamExample")
    sqlContext = SQLContext(sc)

    # $example on$
    # Prepare training data from a list of (label, features) tuples.
    training = sqlContext.createDataFrame([
        (1.0, Vectors.dense([0.0, 1.1, 0.1])),
        (0.0, Vectors.dense([2.0, 1.0, -1.0])),
        (0.0, Vectors.dense([2.0, 1.3, 1.0])),
        (1.0, Vectors.dense([0.0, 1.2, -0.5]))], ["label", "features"])

    # Create a LogisticRegression instance. This instance is an Estimator.
    lr = LogisticRegression(maxIter=10, regParam=0.01)
    # Print out the parameters, documentation, and any default values.
    print "LogisticRegression parameters:\n" + lr.explainParams() + "\n"

    # Learn a LogisticRegression model. This uses the parameters stored in lr.
    model1 = lr.fit(training)

    # Since model1 is a Model (i.e., a transformer produced by an Estimator),
    # we can view the parameters it used during fit().
    # This prints the parameter (name: value) pairs, where names are unique IDs for this
    # LogisticRegression instance.
    print "Model 1 was fit using parameters: "
    print model1.extractParamMap()

    # We may alternatively specify parameters using a Python dictionary as a paramMap
    paramMap = {lr.maxIter: 20}
    paramMap[lr.maxIter] = 30  # Specify 1 Param, overwriting the original maxIter.
    paramMap.update({lr.regParam: 0.1, lr.threshold: 0.55})  # Specify multiple Params.

    # You can combine paramMaps, which are python dictionaries.
    paramMap2 = {lr.probabilityCol: "myProbability"}  # Change output column name
    paramMapCombined = paramMap.copy()
    paramMapCombined.update(paramMap2)

    # Now learn a new model using the paramMapCombined parameters.
    # paramMapCombined overrides all parameters set earlier via lr.set* methods.
    model2 = lr.fit(training, paramMapCombined)
    print "Model 2 was fit using parameters: "
    print model2.extractParamMap()

    # Prepare test data
    test = sqlContext.createDataFrame([
        (1.0, Vectors.dense([-1.0, 1.5, 1.3])),
        (0.0, Vectors.dense([3.0, 2.0, -0.1])),
        (1.0, Vectors.dense([0.0, 2.2, -1.5]))], ["label", "features"])

    # Make predictions on test data using the Transformer.transform() method.
    # LogisticRegression.transform will only use the 'features' column.
    # Note that model2.transform() outputs a "myProbability" column instead of the usual
    # 'probability' column since we renamed the lr.probabilityCol parameter previously.
    prediction = model2.transform(test)
    selected = prediction.select("features", "label", "myProbability", "prediction")
    for row in selected.collect():
        print row
    # $example off$

    sc.stop()
