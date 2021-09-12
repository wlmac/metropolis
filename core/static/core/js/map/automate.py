d = open("data.txt", "r")
data = d.read()
data_list = data.split("\n")
geojson = open("data.geojson", "w")

geojson.write("{\n 'features' : [\n")
for i in data_list:
    featuresList = {}
    line = i[1:len(i)-1].split(",")
    for x in line:
        k,v = x.strip().split(":")
        featuresList[k.strip()] = v.strip()
        print("feature: "+k.strip()+" "+featuresList[k.strip()])
    print(i)
    geojson.write("{\n\t'type': 'Feature',\n\t'geometry':{\n\t\t'type':'Point',\n\t\t'coordinates': ["+featuresList['longitude'][0:-1]+", "+ featuresList['latitude']+"]\n\t},\n\t'properties':{\n\t\t'id':"+featuresList['id']+",\n\t\t'title':"+featuresList['room']+",\n\t\t'floor':"+featuresList['floor']+"\n\t}\n},\n")

geojson.write("],\n'type': 'FeatureCollection'\n}")