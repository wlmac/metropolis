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
    geojson.write('{\n\ttype: "Feature",\n\tgeometry:{\n\t\ttype:"Point",\n\t\tcoordinates: ['+featuresList['longitude'][0:-1]+', '+ featuresList['latitude']+']\n\t},\n\tproperties:{\n\t\tid:"'+featuresList['id']+'",\n\t\troom:'+featuresList['room']+',\n\t\tfloor:'+featuresList['floor']+'\n\t}\n},\n')

geojson.write("]}")
