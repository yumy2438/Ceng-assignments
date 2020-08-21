#include "Scene.h"
#include "Camera.h"
#include "Light.h"
#include "Material.h"
#include "Shape.h"
#include "tinyxml2.h"
#include <limits>
#include "Image.h"
#include <cmath>
#include <thread>

using namespace tinyxml2;

/* 
 * Must render the scene from each camera's viewpoint and create an image.
 * You can use the methods of the Image class to save the image as a PPM file. 
 */
int object_s;
int light_s;

Camera *firstC;	
Image *img;				
Vector3f Scene::rec_mir(const Ray& ray, const int& depth) {int devam;
					float leno,leno2,leno3,len, maxil,cosa,cosalfa;
					Vector3f wi,wo,wiwo,h,wie,wo_f,wr;
	Vector3f colori;
	colori.x=backgroundColor.r;
	colori.y=backgroundColor.g;
	colori.z=backgroundColor.b;
	int tmin=std::numeric_limits<std::int32_t>::max();;
	Shape *obj=NULL;
	ReturnVal ret;
	for(int i=0;i<object_s;i++) {
		Shape *obje=objects[i];
		ReturnVal reti=obje->intersect(ray);
		float reti_t = reti.t;
		if(reti.is_intersected && reti_t<tmin) {
				tmin=reti_t;
				obj=obje;
				ret=reti;
		}
	}
	if(obj) {

		Vector3f ret_intersection_point = ret.intersection_point;
		Vector3f ret_surface_normal = ret.surface_normal;
	    Material *mat=materials[obj->matIndex-1];
	    Vector3f *ambRef = &(mat->ambientRef);
		colori.x=(ambRef->r)*ambientLight.r;
		colori.y=(ambRef->g)*ambientLight.g;
		colori.z=(ambRef->b)*ambientLight.b;
		for(int l=0;l<light_s;l++) {
					int devam=1;
					Vector3f wi_1=sub(lights[l]->position,ret_intersection_point);
					wi = normalize(wi_1);
					wie=scalar_product(wi,shadowRayEps);
					Vector3f wo_1=scalar_product(ray.direction,-1);
					wo = normalize(wo_1);
					Ray *rayo=new Ray(sum(ret_intersection_point,wie),wi);
					for(int ob=0;ob<object_s;ob++) {
						Shape *objer=objects[ob];
						ReturnVal reto=objer->intersect(*rayo);
						if(reto.is_intersected && rayo->gett(lights[l]->position)>=(reto.t)) {
							devam=0;
							break;
						}
					}
					if(devam==0) continue;
					Vector3f sabit=mat->diffuseRef;
					Vector3f sabit2=mat->specularRef;
					Vector3f light_cont=lights[l]->computeLightContribution(ret_intersection_point);
					maxil=max(0.0f,dot_product(wi,ret_surface_normal));
					Vector3f ld;
					ld.x=sabit.x*maxil*light_cont.x;
					ld.y=sabit.y*maxil*light_cont.y;
					ld.z=sabit.z*maxil*light_cont.z;
					wiwo=sum(wi,wo);
					h = normalize(wiwo);
					cosalfa=pow(max(0.0f,dot_product(h,ret_surface_normal)),mat->phongExp);
					Vector3f ls;
					ls.x=sabit2.x*cosalfa*light_cont.x;
					ls.y=sabit2.y*cosalfa*light_cont.y;
					ls.z=sabit2.z*cosalfa*light_cont.z;
					Vector3f ara=sum(ld,ls);
					Vector3f ara2=sum(ara,colori);
					colori.x=ara2.x;
					colori.y=ara2.y;
					colori.z=ara2.z;

				}
				Vector3f mat_mirror_ref = mat->mirrorRef;
				if(depth>0 && dot_product(mat_mirror_ref,mat_mirror_ref)>0) {
					wo_f;
					wo_f=sub(ray.origin, ret.intersection_point);
					leno3=sqrt(dot_product(wo_f,wo_f));
					wo_f.x=wo_f.x/leno3;
					wo_f.y=wo_f.y/leno3;
					wo_f.z=wo_f.z/leno3;
					cosa=dot_product(ret.surface_normal,wo_f)*2;
					wr=sum(scalar_product(wo_f,-1),scalar_product(ret.surface_normal,cosa));
					len=sqrt(dot_product(wr,wr));
					wr.x=wr.x/len;
					wr.y=wr.y/len;
					wr.z=wr.z/len;
					Ray *ray1=new Ray(sum(ret.intersection_point,scalar_product(wr,shadowRayEps)),wr);
					Ray ray=*ray1;

					colori=sum(colori,ikili(mat_mirror_ref,rec_mir(ray,depth-1)));
				}

	}
	return colori;

}

void Scene::th_f(int y) {
	Vector3f clr;
	Color color;
	Ray ray;
	int x;
	int nx = firstC->imgPlane.nx;
		for(x=0;x<nx;x++) {
			ray=firstC->getPrimaryRay(x,y);
			clr=rec_mir(ray,maxRecursionDepth);
			clr.x=min(float(255.0),clr.x);
			clr.y=min(float(255.0),clr.y);
			clr.z=min(float(255.0),clr.z);

			color.red=clr.x;
			color.grn=clr.y;
			color.blu=clr.z;

				img->setPixelValue(x,y,color);
			}

}

void Scene::renderScene(void)
{
	object_s=objects.size();
	light_s=lights.size();
	for(int cam=0;cam<cameras.size();cam++) {
	firstC=cameras[cam];
	ImagePlane img_plane = firstC->imgPlane;
	int ny = img_plane.ny;
	int nx = img_plane.nx;
	img=new Image(nx,ny);
	int x,y;
	int ny1=ny%16;
		for(y=0;y<ny1;y++) {
			th_f(y);
		}
	for(;y<ny;y+=16) {
			thread th1(&Scene::th_f,this,  y);
			thread th2(&Scene::th_f,this, y+1);
			thread th3(&Scene::th_f,this,  y+2);
			thread th4(&Scene::th_f,this, y+3);
			thread th5(&Scene::th_f,this,  y+4);
			thread th6(&Scene::th_f,this, y+5);
			thread th7(&Scene::th_f,this,  y+6);
			thread th8(&Scene::th_f,this, y+7);
			thread th9(&Scene::th_f,this,  y+8);
			thread th10(&Scene::th_f,this, y+9);
			thread th11(&Scene::th_f,this,  y+10);
			thread th12(&Scene::th_f,this, y+11);
			thread th13(&Scene::th_f,this,  y+12);
			thread th14(&Scene::th_f,this, y+13);
			thread th15(&Scene::th_f,this,  y+14);
			thread th16(&Scene::th_f,this, y+15);
			th1.join();
			th2.join();
			th3.join();
			th4.join();
			th5.join();
			th6.join();
			th7.join();
			th8.join();
			th9.join();
			th10.join();
			th11.join();
			th12.join();
			th13.join();
			th14.join();
			th15.join();
			th16.join();
	
	}
		img->saveImage(firstC->imageName);	
	}
	/***********************************************
     *                                             *
	 * TODO: Implement this function               *
     *                                             *
     ***********************************************
	 */
}

// Parses XML file. 
Scene::Scene(const char *xmlPath)
{
	const char *str;
	XMLDocument xmlDoc;
	XMLError eResult;
	XMLElement *pElement;

	

	maxRecursionDepth = 1;
	shadowRayEps = 0.001;

	eResult = xmlDoc.LoadFile(xmlPath);

	XMLNode *pRoot = xmlDoc.FirstChild();

	pElement = pRoot->FirstChildElement("MaxRecursionDepth");
	if(pElement != nullptr)
		pElement->QueryIntText(&maxRecursionDepth);

	pElement = pRoot->FirstChildElement("BackgroundColor");
	str = pElement->GetText();
	sscanf(str, "%f %f %f", &backgroundColor.r, &backgroundColor.g, &backgroundColor.b);

	pElement = pRoot->FirstChildElement("ShadowRayEpsilon");
	if(pElement != nullptr)
		pElement->QueryFloatText(&shadowRayEps);

	pElement = pRoot->FirstChildElement("IntersectionTestEpsilon");
	if(pElement != nullptr)
		eResult = pElement->QueryFloatText(&intTestEps);

	// Parse cameras
	pElement = pRoot->FirstChildElement("Cameras");
	XMLElement *pCamera = pElement->FirstChildElement("Camera");
	XMLElement *camElement;
	while(pCamera != nullptr)
	{
        int id;
        char imageName[64];
        Vector3f pos, gaze, up;
        ImagePlane imgPlane;

		eResult = pCamera->QueryIntAttribute("id", &id);
		camElement = pCamera->FirstChildElement("Position");
		str = camElement->GetText();
		sscanf(str, "%f %f %f", &pos.x, &pos.y, &pos.z);
		camElement = pCamera->FirstChildElement("Gaze");
		str = camElement->GetText();
		sscanf(str, "%f %f %f", &gaze.x, &gaze.y, &gaze.z);
		camElement = pCamera->FirstChildElement("Up");
		str = camElement->GetText();
		sscanf(str, "%f %f %f", &up.x, &up.y, &up.z);
		camElement = pCamera->FirstChildElement("NearPlane");
		str = camElement->GetText();
		sscanf(str, "%f %f %f %f", &imgPlane.left, &imgPlane.right, &imgPlane.bottom, &imgPlane.top);
		camElement = pCamera->FirstChildElement("NearDistance");
		eResult = camElement->QueryFloatText(&imgPlane.distance);
		camElement = pCamera->FirstChildElement("ImageResolution");	
		str = camElement->GetText();
		sscanf(str, "%d %d", &imgPlane.nx, &imgPlane.ny);
		camElement = pCamera->FirstChildElement("ImageName");
		str = camElement->GetText();
		strcpy(imageName, str);

		cameras.push_back(new Camera(id, imageName, pos, gaze, up, imgPlane));

		pCamera = pCamera->NextSiblingElement("Camera");
	}

	// Parse materals
	pElement = pRoot->FirstChildElement("Materials");
	XMLElement *pMaterial = pElement->FirstChildElement("Material");
	XMLElement *materialElement;
	while(pMaterial != nullptr)
	{
		materials.push_back(new Material());

		int curr = materials.size() - 1;
	
		eResult = pMaterial->QueryIntAttribute("id", &materials[curr]->id);
		materialElement = pMaterial->FirstChildElement("AmbientReflectance");
		str = materialElement->GetText();
		sscanf(str, "%f %f %f", &materials[curr]->ambientRef.r, &materials[curr]->ambientRef.g, &materials[curr]->ambientRef.b);
		materialElement = pMaterial->FirstChildElement("DiffuseReflectance");
		str = materialElement->GetText();
		sscanf(str, "%f %f %f", &materials[curr]->diffuseRef.r, &materials[curr]->diffuseRef.g, &materials[curr]->diffuseRef.b);
		materialElement = pMaterial->FirstChildElement("SpecularReflectance");
		str = materialElement->GetText();
		sscanf(str, "%f %f %f", &materials[curr]->specularRef.r, &materials[curr]->specularRef.g, &materials[curr]->specularRef.b);
		materialElement = pMaterial->FirstChildElement("MirrorReflectance");
		if(materialElement != nullptr)
		{
			str = materialElement->GetText();
			sscanf(str, "%f %f %f", &materials[curr]->mirrorRef.r, &materials[curr]->mirrorRef.g, &materials[curr]->mirrorRef.b);
		}
				else
		{
			materials[curr]->mirrorRef.r = 0.0;
			materials[curr]->mirrorRef.g = 0.0;
			materials[curr]->mirrorRef.b = 0.0;
		}
		materialElement = pMaterial->FirstChildElement("PhongExponent");
		if(materialElement != nullptr)
			materialElement->QueryIntText(&materials[curr]->phongExp);

		pMaterial = pMaterial->NextSiblingElement("Material");
	}

	// Parse vertex data
	pElement = pRoot->FirstChildElement("VertexData");
	int cursor = 0;
	Vector3f tmpPoint;
	str = pElement->GetText();
	while(str[cursor] == ' ' || str[cursor] == '\t' || str[cursor] == '\n')
		cursor++;
	while(str[cursor] != '\0')
	{
		for(int cnt = 0 ; cnt < 3 ; cnt++)
		{
			if(cnt == 0)
				tmpPoint.x = atof(str + cursor);
			else if(cnt == 1)
				tmpPoint.y = atof(str + cursor);
			else
				tmpPoint.z = atof(str + cursor);
			while(str[cursor] != ' ' && str[cursor] != '\t' && str[cursor] != '\n')
				cursor++; 
			while(str[cursor] == ' ' || str[cursor] == '\t' || str[cursor] == '\n')
				cursor++;
		}
		vertices.push_back(tmpPoint);
	}
	// Parse objects
	pElement = pRoot->FirstChildElement("Objects");
	
	// Parse spheres
	XMLElement *pObject = pElement->FirstChildElement("Sphere");
	XMLElement *objElement;
	while(pObject != nullptr)
	{
		int id;
		int matIndex;
		int cIndex;
		float R;

		eResult = pObject->QueryIntAttribute("id", &id);
		objElement = pObject->FirstChildElement("Material");
		eResult = objElement->QueryIntText(&matIndex);
		objElement = pObject->FirstChildElement("Center");
		eResult = objElement->QueryIntText(&cIndex);
		objElement = pObject->FirstChildElement("Radius");
		eResult = objElement->QueryFloatText(&R);
		objects.push_back(new Sphere(id, matIndex, cIndex, R, &vertices));
		pObject = pObject->NextSiblingElement("Sphere");
	}

	// Parse triangles
	pObject = pElement->FirstChildElement("Triangle");
	while(pObject != nullptr)
	{
		int id;
		int matIndex;
		int p1Index;
		int p2Index;
		int p3Index;

		eResult = pObject->QueryIntAttribute("id", &id);
		objElement = pObject->FirstChildElement("Material");
		eResult = objElement->QueryIntText(&matIndex);
		objElement = pObject->FirstChildElement("Indices");
		str = objElement->GetText();
		sscanf(str, "%d %d %d", &p1Index, &p2Index, &p3Index);

		objects.push_back(new Triangle(id, matIndex, p1Index, p2Index, p3Index, &vertices));

		pObject = pObject->NextSiblingElement("Triangle");
	}

	// Parse meshes
	pObject = pElement->FirstChildElement("Mesh");
	while(pObject != nullptr)
	{
		int id;
		int matIndex;
		int p1Index;
		int p2Index;
		int p3Index;
		int cursor = 0;
		int vertexOffset = 0;
		vector<Triangle> faces;
		vector<int> *meshIndices = new vector<int>;

		eResult = pObject->QueryIntAttribute("id", &id);
		objElement = pObject->FirstChildElement("Material");
		eResult = objElement->QueryIntText(&matIndex);
		objElement = pObject->FirstChildElement("Faces");
		objElement->QueryIntAttribute("vertexOffset", &vertexOffset);
		str = objElement->GetText();
		while(str[cursor] == ' ' || str[cursor] == '\t' || str[cursor] == '\n')
			cursor++;
		while(str[cursor] != '\0')
		{
			for(int cnt = 0 ; cnt < 3 ; cnt++)
			{
				if(cnt == 0)
					p1Index = atoi(str + cursor) + vertexOffset;
				else if(cnt == 1)
					p2Index = atoi(str + cursor) + vertexOffset;
				else
					p3Index = atoi(str + cursor) + vertexOffset;
				while(str[cursor] != ' ' && str[cursor] != '\t' && str[cursor] != '\n')
					cursor++; 
				while(str[cursor] == ' ' || str[cursor] == '\t' || str[cursor] == '\n')
					cursor++;
			}
			faces.push_back(*(new Triangle(-1, matIndex, p1Index, p2Index, p3Index, &vertices)));
			meshIndices->push_back(p1Index);
			meshIndices->push_back(p2Index);
			meshIndices->push_back(p3Index);
		}

		objects.push_back(new Mesh(id, matIndex, faces, meshIndices, &vertices));

		pObject = pObject->NextSiblingElement("Mesh");
	}

	// Parse lights
	int id;
	Vector3f position;
	Vector3f intensity;
	pElement = pRoot->FirstChildElement("Lights");

	XMLElement *pLight = pElement->FirstChildElement("AmbientLight");
	XMLElement *lightElement;
	str = pLight->GetText();
	sscanf(str, "%f %f %f", &ambientLight.r, &ambientLight.g, &ambientLight.b);

	pLight = pElement->FirstChildElement("PointLight");
	while(pLight != nullptr)
	{
		eResult = pLight->QueryIntAttribute("id", &id);
		lightElement = pLight->FirstChildElement("Position");
		str = lightElement->GetText();
		sscanf(str, "%f %f %f", &position.x, &position.y, &position.z);
		lightElement = pLight->FirstChildElement("Intensity");
		str = lightElement->GetText();
		sscanf(str, "%f %f %f", &intensity.r, &intensity.g, &intensity.b);

		lights.push_back(new PointLight(position, intensity));

		pLight = pLight->NextSiblingElement("PointLight");
	}
}

