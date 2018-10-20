import csv;
import numpy;
RATINGS_FILE='Documents\Ratings.csv'
MEANS_FILE='Documents\Means.csv'
SMARTNESS_FILE='Documents\Smartness.csv'
OVERALL_SMARTNESS_FILE='Documents\OverallSmartness.csv'
OVERALL_RATINGS_FILE='Documents\OverallRatings.csv'
DIRECTION_OF_CHANGE_FILE='Documents\DirectionOfChange.csv'
CORRELATION_FILE='Documents\Correlations.csv'
K_FACTOR=0.0001;
LAMBDA=0.00000001;
def convertValueCsvIntoDict(csvfilelocation):
    products={};
    with open(csvfilelocation, 'rb') as csvfile:
        frequencies = list(csv.reader(csvfile));
        csvfile.close();
        for row in frequencies[1:len(frequencies)]:
            row=list(row);
            if row[0] in products.keys():
                attributes=products[row[0]];
                if row[1] in attributes.keys():
                    attributes[row[1]][row[2]]=int(row[3]);
                else:
                    attributes[row[1]]={row[2]:int(row[3])};
            else:
                products[row[0]]={row[1]:{row[2]:int(row[3])}};
    return products;
def getMeansFromCsv(meansfile):
    with open(meansfile, 'rb') as csvfile:
        means = list(csv.reader(csvfile));
        csvfile.close();
    meansdict = {};
    for row in means:
        if row[0] not in meansdict.keys():
            meansdict[row[0]]={};
        meansdict[row[0]][row[1]]=float(row[2]);
    return meansdict;
def getNormRatingsFromCsv(ratingsfile):
    products={};
    with open(ratingsfile, 'rb') as csvfile:
        ratings = list(csv.reader(csvfile));
        csvfile.close();
    for row in ratings:
        row=list(row);
        if row[0] in products.keys():
            attributes=products[row[0]];
            if row[1] in attributes.keys():
                attributes[row[1]][row[2]]=float(row[3]);
            else:
                attributes[row[1]]={row[2]:float(row[3])};
        else:
            products[row[0]]={row[1]:{row[2]:float(row[3])}};
    return products;
def getOverallRatingFromCsv(overallratingsfile):
    attributes={};
    with open(overallratingsfile, 'rb') as csvfile:
        frequencies = list(csv.reader(csvfile));
        csvfile.close();
        for row in frequencies:
            if row[0] in attributes.keys():
                attributes[row[0]][row[1]]=float(row[2]);
            else:
                attributes[row[0]]={row[1]:float(row[2])};
    return attributes;
def getSmartnessFromCsv(smartnessfile):
    smartness={};
    with open(smartnessfile, 'rb') as csvfile:
        frequencies = list(csv.reader(csvfile));
        csvfile.close();
        for row in frequencies[1:len(frequencies)]:
            row=list(row);
            if row[0] in smartness.keys():
                attributes=smartness[row[0]];
                if row[1] in attributes.keys():
                    attributes[row[1]][row[2]]=float(row[3]);
                else:
                    attributes[row[1]]={row[2]:float(row[3])};
            else:
                smartness[row[0]]={row[1]:{row[2]:float(row[3])}};
    return smartness;
def convertDictIntoRatingCsv(dictionary,csvfilelocation):
    with open(csvfilelocation, 'wb') as csvfile:
        scores = csv.writer(csvfile)
        for vendor in sorted(dictionary.keys()):
            for attribute in sorted(dictionary[vendor].keys()):
                temp = numpy.mean(dictionary[vendor][attribute].values());
                for item in sorted(dictionary[vendor][attribute].items(),key = lambda x:x[1],reverse=True):
                    scores.writerow([vendor, attribute, item[0], item[1]/temp]);
        csvfile.close();
def convertDictIntoAttributeCsv(dictionary,csvfilelocation):
    with open(csvfilelocation, 'wb') as csvfile:
        scores = csv.writer(csvfile)
        for vendor in sorted(dictionary.keys()):
            mu={};
            sigma={};
            for attribute in dictionary[vendor].keys():
                mu[attribute] = numpy.mean(dictionary[vendor][attribute].values());
                sigma[attribute] = numpy.mean(map(lambda x:(x-mu[attribute])**2,dictionary[vendor][attribute].values()))/mu[attribute]**2;
            for item in sorted(sigma.items(),key = lambda x:x[1],reverse=True):
                scores.writerow([vendor, item[0], mu[item[0]]]);
        csvfile.close();
def convertDictIntoOverallCsv(dictionary,csvfilelocation):
    with open(csvfilelocation, 'wb') as csvfile:
        scores = csv.writer(csvfile)
        for attribute in sorted(dictionary.keys()):
            for item in sorted(dictionary[attribute].items(),key = lambda x:x[1],reverse=True):
                scores.writerow([attribute, item[0], item[1]]);
        csvfile.close();
def convertDictIntoSmartnessCsv(dictionary,csvfilelocation):
    with open(csvfilelocation, 'wb') as csvfile:
        scores = csv.writer(csvfile)
        for vendor in sorted(dictionary.keys()):
            for attribute in sorted(dictionary[vendor].keys()):
                for item in sorted(dictionary[vendor][attribute].items(),key = lambda x:x[1],reverse=True):
                    scores.writerow([vendor, attribute, item[0], item[1]]);
        csvfile.close();
def convertDictIntoOverallSmartnessCsv(overallsmartness,csvfilelocation):
    with open(csvfilelocation, 'wb') as csvfile:
        scores = csv.writer(csvfile)
        for vendor in sorted(overallsmartness.keys()):
            for item in sorted(overallsmartness[vendor].items(),key = lambda x:x[1],reverse=True):
                    scores.writerow([vendor, item[0], item[1]]);
        csvfile.close();
def normaliseRating(ratings):
    normratings={};
    means={};
    for vendor in ratings.keys():
        normratings[vendor]={};
        means[vendor]={};
        for attribute in ratings[vendor].keys():
            normratings[vendor][attribute] = {};
            means[vendor][attribute] = numpy.mean(ratings[vendor][attribute].values());
            for value in ratings[vendor][attribute].keys():
                normratings[vendor][attribute][value] = ratings[vendor][attribute][value]/means[vendor][attribute];
    return [normratings, means];
def calculateWeightedRating(dict1,w1,dict2,w2):
    dict3={};
    for vendor in dict1.keys():
        dict3[vendor]={};
        for attribute in dict1[vendor].keys():
            dict3[vendor][attribute]={};
            for key in dict1[vendor][attribute].keys():
                if vendor in dict2.keys() and attribute in dict2[vendor].keys() and key in dict2[vendor][attribute].keys():
                    dict3[vendor][attribute][key]=w1*dict1[vendor][attribute][key]+w2*dict2[vendor][attribute][key];
                else:
                    dict3[vendor][attribute][key]=w1*dict1[vendor][attribute][key];
    for vendor in dict2.keys():
        if vendor not in dict1.keys():
            dict3[vendor]={};
        for attribute in dict2[vendor].keys():
            if vendor not in dict1.keys() or attribute not in dict1[vendor].keys():
                dict3[vendor][attribute]={};
            for key in dict2[vendor][attribute].keys():
                if vendor not in dict1.keys() or attribute not in dict1[vendor].keys() or key not in dict1[vendor][attribute].keys():
                    dict3[vendor][attribute][key]=w2*dict2[vendor][attribute][key];
    return dict3;
def calculateRatingGivenNewnOldData(newdata,w_new,olddata,w_old):
    '''
    w_old is weightage of old data only
    w_new is weightage of newer data (in newdata but not in olddata)
    '''
    dict3={};
    for vendor in newdata.keys():
        dict3[vendor]={};
        for attribute in newdata[vendor].keys():
            dict3[vendor][attribute]={};
            for key in newdata[vendor][attribute].keys():
                if vendor in olddata.keys() and attribute in olddata[vendor].keys() and key in olddata[vendor][attribute].keys():
                    dict3[vendor][attribute][key]=w_new*max(newdata[vendor][attribute][key]-olddata[vendor][attribute][key],0)+w_old*olddata[vendor][attribute][key];
                else:
                    dict3[vendor][attribute][key]=w_new*newdata[vendor][attribute][key];
    for vendor in olddata.keys():
        if vendor not in newdata.keys():
            dict3[vendor]={};
        for attribute in olddata[vendor].keys():
            if vendor not in newdata.keys() or attribute not in newdata[vendor].keys():
                dict3[vendor][attribute]={};
            for key in olddata[vendor][attribute].keys():
                if vendor not in newdata.keys() or attribute not in newdata[vendor].keys() or key not in newdata[vendor][attribute].keys():
                    dict3[vendor][attribute][key]=w_old*olddata[vendor][attribute][key];
    return dict3;
def updatedRating(datatoday,datayesterday,ratingyesterday,decayfactor):
    newdata=calculateRatingGivenNewnOldData(datatoday,1,datayesterday,0);
    return calculateWeightedRating(newdata,1,ratingyesterday,decayfactor);
def initialRating(listofdata,decayfactor):
    '''
    listofdata is a list having data dictionaries, newest first
    '''
    templist=listofdata[:];
    templist.reverse();
    rating=templist[0];
    for i in range(1,len(listofdata)):
        rating=updatedRating(templist[i],templist[i-1],rating,decayfactor);
    return rating;
def vendorIndependentNormRating(ratings, means):
    overallratings={};
    normfactorsforattributes={};
    for vendor in ratings.keys():
        for attribute in ratings[vendor].keys():
            if attribute not in normfactorsforattributes.keys():
                normfactorsforattributes[attribute]=0;
            normfactorsforattributes[attribute]+=means[vendor][attribute];
            if attribute not in overallratings.keys():
                overallratings[attribute]={};
            for value in ratings[vendor][attribute].keys():
                if value not in overallratings[attribute].keys():
                    overallratings[attribute][value]=0;
                overallratings[attribute][value]+=ratings[vendor][attribute][value];
    for attribute in overallratings.keys():
        temp = normfactorsforattributes[attribute];
        for value in overallratings[attribute].keys():
            overallratings[attribute][value] = overallratings[attribute][value]/temp;
    return overallratings;
def calculateMismatch(k_factor, normratings, overallratings):
    matchratings={};
    for vendor in normratings.keys():
        matchratings[vendor]={};
        for attribute in normratings[vendor].keys():
            matchratings[vendor][attribute]={};
            for value in normratings[vendor][attribute].keys():
                matchratings[vendor][attribute][value]=-k_factor*(normratings[vendor][attribute][value]-overallratings[attribute][value])**2;
    return matchratings;
def calculateAttributeLevelSmartness(smartness):
    means={};
    for vendor in smartness.keys():
        means[vendor]={};
        for attribute in smartness[vendor].keys():
            means[vendor][attribute]=numpy.mean(smartness[vendor][attribute].values());
    return means;
def updatedSmartness(oldsmartness, k_factor, normratings, oldnormratings, overallratings, oldoverallratings):
    smartness={};
    for vendor in normratings.keys():
        smartness[vendor]={};
        for attribute in normratings[vendor].keys():
            smartness[vendor][attribute]={};
            for value in normratings[vendor][attribute].keys():
                if vendor in oldnormratings.keys() and attribute in oldnormratings[vendor].keys() and value in oldnormratings[vendor][attribute].keys():
                    smartness[vendor][attribute][value]=oldsmartness[vendor][attribute][value]+(oldnormratings[vendor][attribute][value]-oldoverallratings[attribute][value])*(overallratings[attribute][value]-oldoverallratings[attribute][value])-k_factor*(normratings[vendor][attribute][value]-overallratings[attribute][value])**2;
                else:
                    smartness[vendor][attribute][value]=-k_factor*(normratings[vendor][attribute][value]-overallratings[attribute][value])**2;
    return smartness;
def calculateDirectionOfChange(overallsmartness, normratings, means, overallratings):
    doc={};
    for vendor in normratings.keys():
        for attribute in normratings[vendor].keys():
            if attribute not in doc.keys():
                doc[attribute]={};
            for value in normratings[vendor][attribute].keys():
                if value not in doc[attribute].keys():
                    doc[attribute][value]=0;
                #doc[attribute][value]+=overallsmartness[vendor][attribute]*means[vendor][attribute]*(normratings[vendor][attribute][value]-overallratings[attribute][value]);
                doc[attribute][value]+=overallsmartness[vendor][attribute]*normratings[vendor][attribute][value];
    return doc;
def calculateCorrelation(directionofchange, oldoverallratings, newoverallratings):
    expected=[];
    actual=[];
    for attribute in sorted(directionofchange.keys()):
        for value in sorted(directionofchange[attribute].keys()):
            expected.append(directionofchange[attribute][value]);
            actual.append(newoverallratings[attribute][value]-oldoverallratings[attribute][value]);
    corr=numpy.corrcoef(expected,actual);
    return corr[1][0];
def calculateDistance(directionofchange, oldoverallratings, newoverallratings):
    expected=[];
    actual=[];
    for attribute in sorted(directionofchange.keys()):
        for value in sorted(directionofchange[attribute].keys()):
            expected.append(directionofchange[attribute][value]);
            actual.append(newoverallratings[attribute][value]-oldoverallratings[attribute][value]);
    dist=numpy.linalg.norm(numpy.array(expected)-numpy.array(actual));
    return dist;
def calculateFit(directionofchange, oldoverallratings, newoverallratings):
    expected=[];
    actual=[];
    for attribute in sorted(directionofchange.keys()):
        for value in sorted(directionofchange[attribute].keys()):
            expected.append(directionofchange[attribute][value]);
            actual.append(newoverallratings[attribute][value]-oldoverallratings[attribute][value]);
    fitdata=[int(x<=0.5) for x in abs((numpy.array(expected)-numpy.array(actual))/numpy.array(actual))];
    fit=float(sum(fitdata))/float(len(fitdata));
    return fit;
inputfile=raw_input("Enter location of input file:");
with open(inputfile,'rb') as fp:
    decay_factor=float(fp.readline().strip());
    n=int(fp.readline().strip());
#print "Enter all "+str(n)+" csv file locations (newest data first).";
    listofdata=[];
    for i in range(n):
        listofdata.append(convertValueCsvIntoDict(fp.readline().strip()));
    k = K_FACTOR;
    ratings = [];
    normratings = [];
    overallratings = [];
#for k in [0.001*i for i in range(100)]:
    ######INITIALISATION######
    ratings.append(initialRating([listofdata[n-1]],decay_factor));
    normratings.append([]);
    [normratings[0], means] = normaliseRating(ratings[0]);
    overallratings.append(vendorIndependentNormRating(ratings[0], means));
    smartness=calculateMismatch(k, normratings[0], overallratings[0]);
    overallsmartness=calculateAttributeLevelSmartness(smartness);
    directionofchange=calculateDirectionOfChange(overallsmartness, normratings[0], means, overallratings[0]);
    correlations=[];
    ######ITERATION######
    for i in range(n-1,0,-1):
        ratings.append(updatedRating(listofdata[i-1], listofdata[i], ratings[n-1-i], decay_factor));
        oldnormratings = normratings[n-1-i];
        normratings.append([]);
        [normratings[n-i], means] = normaliseRating(ratings[n-i]);
        oldoverallratings=overallratings[n-1-i];
        overallratings.append(vendorIndependentNormRating(ratings[n-i], means));
        correlations.append(calculateCorrelation(directionofchange, oldoverallratings, overallratings[n-i]));
        smartness=updatedSmartness(smartness, k, normratings[n-i], oldnormratings, overallratings[n-i], oldoverallratings);
        overallsmartness=calculateAttributeLevelSmartness(smartness);
        directionofchange=calculateDirectionOfChange(overallsmartness, normratings[n-i], means, overallratings[n-i]);
    parameters=[];
    for vendor in means.keys():
        for attribute in means[vendor].keys():
            parameters.append([vendor, attribute]);
    X=[];
    y=[];
    for i in range(n-3):
        for attribute in overallratings[i+1].keys():
            for value in overallratings[i+1][attribute].keys():
                y.append([overallratings[i+1][attribute][value]-overallratings[i].get(attribute,{value:0}).get(value,0)]);
                temp=[];
                for pair in parameters:
                    if pair[1] == attribute:
                        temp.append(normratings[i].get(pair[0],{attribute:{value:0}}).get(attribute,{value:0}).get(value,0));
                    else:
                        temp.append(0);
                X.append(temp);
    trainingdata = numpy.matrix(X);
    answerdata = numpy.matrix(y);
    regularisationmatrix = numpy.matrix(numpy.identity(len(parameters)));
    #regularisationmatrix[0][0]=0;
    theta = numpy.linalg.inv(trainingdata.transpose()*trainingdata+LAMBDA*regularisationmatrix)*trainingdata.transpose()*answerdata;
    trainedparameters=theta.transpose().tolist()[0];
    #print trainedparameters[0];
    overallsmartness={};
    for i in range(0,len(parameters)):
        pair=parameters[i];
        if pair[0] not in overallsmartness.keys():
            overallsmartness[pair[0]]={};
        overallsmartness[pair[0]][pair[1]]=trainedparameters[i];
    [normratings[0], means] = normaliseRating(ratings[0]);
    directionofchange=calculateDirectionOfChange(overallsmartness, normratings[0], means, overallratings[0]);
    correlations=[];
    distances=[];
    fits=[];
    ######ITERATION######
    for i in range(n-1,0,-1):
        [normratings[n-i], means] = normaliseRating(ratings[n-i]);
        oldoverallratings=overallratings[n-1-i];
        correlations.append(calculateCorrelation(directionofchange, oldoverallratings, overallratings[n-i]));
        distances.append(calculateDistance(directionofchange, oldoverallratings, overallratings[n-i]));
        fits.append(calculateFit(directionofchange, oldoverallratings, overallratings[n-i]));
        directionofchange=calculateDirectionOfChange(overallsmartness, normratings[n-i], means, overallratings[n-i]);
    #################valuefile=raw_input("Enter the csv file location for ratings of attribute values:");
    convertDictIntoRatingCsv(ratings[n-1],RATINGS_FILE);
    #################attributefile=raw_input("Enter the csv file location for information of attributes:");
    convertDictIntoAttributeCsv(ratings[n-1],MEANS_FILE);
    convertDictIntoOverallCsv(overallratings[n-1],OVERALL_RATINGS_FILE);
    convertDictIntoSmartnessCsv(smartness,SMARTNESS_FILE);
    convertDictIntoOverallSmartnessCsv(overallsmartness, OVERALL_SMARTNESS_FILE);
    convertDictIntoOverallCsv(directionofchange,DIRECTION_OF_CHANGE_FILE);
    print correlations;
    print distances;
    print fits;