#include <iostream>
#include <iomanip>
#include <cstdlib>
#include <fstream>
#include <cmath>

#include "Scene.h"
#include "Camera.h"
#include "Color.h"
#include "Model.h"
#include "Rotation.h"
#include "Scaling.h"
#include "Translation.h"
#include "Triangle.h"
#include "Vec3.h"
#include "tinyxml2.h"
#include "Helpers.h"
#include <algorithm>

using namespace tinyxml2;
using namespace std;

/*
	Transformations, clipping, culling, rasterization are done here.
	You can define helper functions inside Scene class implementation.
*/

void Scene::setPixel(int x,int y,Color c,int nx,int ny)
{
	if(x<0) return;
	if(x>=nx) return;
	if(y<0) return;
	if(y>=ny) return;
	this->image[x][y].r=int(round(c.r));
	this->image[x][y].g=int(round(c.g));
	this->image[x][y].b=int(round(c.b));
}
Color Scene::calculateColor(Color *c0,Color *c1,int x,int y,int x0,int y0,int x1,int y1,double m)
{
	if(abs(m)>1)//according to y.
	{
		double alfa = double((y-y0))/(y1-y0);
		double r = (1-alfa)*c0->r+alfa*c1->r;
		double g = (1-alfa)*c0->g+alfa*c1->g;
		double b = (1-alfa)*c0->b+alfa*c1->b;
		return Color(r,g,b);
	}
	else//according to x.
	{
		double alfa = double((x-x0))/(x1-x0);
		double r = (1-alfa)*c0->r+alfa*c1->r;
		double g = (1-alfa)*c0->g+alfa*c1->g;
		double b = (1-alfa)*c0->b+alfa*c1->b;
		return Color(r,g,b);

	}
}
double Scene::calculatef(int x,int y,int x0,int y0,int x1,int y1)
{
	return x*(y0-y1)+y*(x1-x0)+x0*y1-y0*x1;
}
bool Scene::visible(double den,double num,double *te,double *tl)
{
	if(den>0)
	{
		//bu t=x1-x0/xmin-x0
		double t = num/den;
		if(t>*tl) return false;
		if(t>*te) *te = t;
	}
	else if(den<0)
	{
		double t = num/den;
		if(t<*te) return false;
		if(t<*tl) *tl = t;
	}
	else if(num>0)
	{
		return false;
	}
	return true;
}

void Scene::drawLine(Matrix4 Mvp,double x0_bef,double y0_bef,double z0_bef,double x1_bef,double y1_bef,double z1_bef,Color c0,Color c1,int nx,int ny)
{
	//vec4 takes a color id, however i should not use color id.!!!!!!!!!!!
	Vec4 edge1(x0_bef,y0_bef,z0_bef,1.0,1.0);
	Vec4 edge2(x1_bef,y1_bef,z1_bef,1.0,1.0);
	Vec4 converted_edge1=multiplyMatrixWithVec4(Mvp,edge1);
	Vec4 converted_edge2=multiplyMatrixWithVec4(Mvp,edge2);
	double slope;
	if(x1_bef==x0_bef)
	{
		slope = 1.5;
	}
	else
	{
		slope = double((y1_bef-y0_bef))/(x1_bef-x0_bef);
	}
	int x0 = round(converted_edge1.x);
	int y0 = round(converted_edge1.y);
	int x1 = round(converted_edge2.x);
	int y1 = round(converted_edge2.y);
	if (slope>0.0 && slope<=1.0) {
		int y=y0;
		if(y1-y0>0)
		{
			for(int x=x0;x<=x1;x++) 
			{
				setPixel(x,y,calculateColor(&c0,&c1,x,y,x0,y0,x1,y1,slope),nx,ny);
				if(calculatef(x+1,y+0.5,x0,y0,x1,y1)<0) y+=1;
			}
		}
		else
		{
			for(int x=x0;x>=x1;x--)
			//draw it.
			{
				setPixel(x,y,calculateColor(&c0,&c1,x,y,x0,y0,x1,y1,slope),nx,ny);
				if(calculatef(x-1,y-0.5,x0,y0,x1,y1)<0) y-=1;
			}

		}

	}
	else if (slope>1.0) {
		int x=x0;
		if(y1-y0>0)
		{
			for(int y=y0;y<=y1;y++)
			{
				setPixel(x,y,calculateColor(&c0,&c1,x,y,x0,y0,x1,y1,slope),nx,ny);
				//draw it.
				if(calculatef(x+0.5,y+1,x0,y0,x1,y1)>0)
				{
					x+=1;
				}
			}
		}
		else
		{
			for(int y=y0;y>=y1;y--)
			{
				setPixel(x,y,calculateColor(&c0,&c1,x,y,x0,y0,x1,y1,slope),nx,ny);
				//draw it.
				if(calculatef(x-0.5,y-1,x0,y0,x1,y1)>0)
				{
					x-=1;
				}
			}

		}
	}
	else if (slope<=0.0 && slope>=-1.0) { 
		int y = y0;
		if (y1-y0>0)
		{
			for(int x=x0;x>=x1;x--)
			//draw it.
			{
				setPixel(x,y,calculateColor(&c0,&c1,x,y,x0,y0,x1,y1,slope),nx,ny);
				if(calculatef(x-1,y+0.5,x0,y0,x1,y1)>0) y+=1;	
			}
		}
		else
		{
			for(int x=x0;x<x1;x++)
			{
				setPixel(x,y,calculateColor(&c0,&c1,x,y,x0,y0,x1,y1,slope),nx,ny);
				if(calculatef(x+1,y-0.5,x0,y0,x1,y1)>0) y-=1;
			}
		}
	}
	else if (slope<-1.0) {
		int x = x0;
		if(y1-y0<0)
		{
			for(int y=y0;y>=y1;y--)
			//draw it.
			{
				setPixel(x,y,calculateColor(&c0,&c1,x,y,x0,y0,x1,y1,slope),nx,ny);
				if(calculatef(x+0.5,y-1,x0,y0,x1,y1)<0)
				{
					x+=1;
				}
			}
		}
		else
		{
			for(int y=y0;y<=y1;y++)
			//draw it.
			{
				setPixel(x,y,calculateColor(&c0,&c1,x,y,x0,y0,x1,y1,slope),nx,ny);
				if(calculatef(x-0.5,y+1,x0,y0,x1,y1)<0)
				{
					x-=1;
				}
			}

		}

	}
}


void Scene::forwardRenderingPipeline(Camera *camera)
{
  Matrix4 Mper;
  int nx = camera->horRes;
  int ny = camera->verRes;
  double n = camera->near;
  double f = camera->far;
  double r = camera->right;
  double l = camera->left;
  double t = camera->top;
  double b = camera->bottom;

  double mper1[4][4] = {{(2*n)/(r-l),0,(r+l)/(r-l),0},{0,(2*n)/(t-b),(t+b)/(t-b),0},{0,0,-1*((f+n)/(f-n)),(-2*f*n)/(f-n)},{0,0,-1,0}};
  double morth[4][4] = {{2/(r-l),0,0,(-r-l)/(r-l)},{0,2/(t-b),0,(-t-b)/(t-b)},{0,0,2/(n-f),(-f-n)/(f-n)},{0,0,0,1}};

  if(projectionType==1)
  {
    Mper = Matrix4(mper1);

  }
  else
  {
    Mper = Matrix4(morth);
  }
	double mcamt[4][4]={{(camera->u).x,(camera->u).y,(camera->u).z,-1*dotProductVec3(camera->u,camera->pos)},{(camera->v).x,(camera->v).y,(camera->v).z,-1*dotProductVec3(camera->v,camera->pos)},{(camera->w).x,(camera->w).y,(camera->w).z,-1*dotProductVec3(camera->w,camera->pos)},{0,0,0,1}};
	Matrix4 Mcam(mcamt);
	double mvpt[4][4]={{(camera->horRes)/2.0,0,0,((camera->horRes)-1)/2.0},{0,(camera->verRes)/2.0,0,((camera->verRes)-1)/2.0},{0,0,0.5,0.5},{0,0,0,1.0}};
	Matrix4 Mvp(mvpt);
	for(int i=0;i<models.size();i++) {
		Model* ourmodel=models[i];	
		Matrix4 multiplieds[ourmodel->numberOfTransformations];
		for(int i2=0;i2<ourmodel->numberOfTransformations;i2++) {
			char transtype=ourmodel->transformationTypes[i2];
			int transid=ourmodel->transformationIds[i2]-1;
			if (transtype=='r') {
				Rotation* rot=this->rotations[transid];
				double ux = rot->ux;
				double uy = rot->uy;
				double uz = rot->uz;

				double vx,vy,vz;
				double wx,wy,wz;
				double angle = rot->angle * M_PI / 180;
				if(abs(ux)<=abs(uy) && abs(ux)<=abs(uz))
				{
					vx = 0;
					vy = -1*uz;
					vz = uy;
				}
				else if(abs(uy)<=abs(uz) && abs(uy)<=abs(ux))
				{
					vy = 0;
					vx = uz;
					vz = -1*ux;
				}
				else
				{
					vz = 0;
					vy = ux;
					vx = -1*uy;
				}


			    wx = uy * vz - vy * uz;
			    wy = vx * uz - ux * vz;
			    wz = ux * vy - vx * uy;

			    double dw=sqrt(wx*wx+wy*wy+wz*wz);
				wx/=dw;
				wy/=dw;
				wz/=dw;
				
				double dv=sqrt(vx*vx+vy*vy+vz*vz);
				vx/=dv;
				vy/=dv;
				vz/=dv;

			    double mforrot[4][4]={{ux,uy,uz,0},{vx,vy,vz,0},{wx,wy,wz,0},{0,0,0,1}};
			    Matrix4 M(mforrot);
			    double minvforrot[4][4]={{ux,vx,wx,0},{uy,vy,wy,0},{uz,vz,wz,0},{0,0,0,1}};
			    Matrix4 Minv(minvforrot);
			    double rotxforrot[4][4]={{1,0,0,0},{0,cos(angle),-1*sin(angle),0},{0,sin(angle),cos(angle),0},{0,0,0,1}};
			    Matrix4 Rotx(rotxforrot);

			    Matrix4 multiplied=multiplyMatrixWithMatrix(Minv,Rotx);
			    multiplied=multiplyMatrixWithMatrix(multiplied,M);
			    multiplieds[i2]=multiplied;
			}
			else if (transtype=='s') 
			{
				Scaling* scal=this->scalings[transid];
				double arr[4][4]={{scal->sx,0,0,0},{0,scal->sy,0,0},{0,0,scal->sz,0},{0,0,0,1}};
				Matrix4 multiplied(arr);
				multiplieds[i2]=multiplied;
			}
			else {
				Translation* transla=this->translations[transid];
				double arr[4][4]={{1,0,0,transla->tx},{0,1,0,transla->ty},{0,0,1,transla->tz},{0,0,0,1}};
				Matrix4 multiplied(arr);
				multiplieds[i2]=multiplied;

			}

		}
		Matrix4 Mmodel=getIdentityMatrix();
		for(int cnt=(ourmodel->numberOfTransformations-1);cnt>=0;cnt--) {
			Mmodel=multiplyMatrixWithMatrix(Mmodel,multiplieds[cnt]);
		}
		Matrix4 MUpToVP(multiplyMatrixWithMatrix(multiplyMatrixWithMatrix(Mper,Mcam),Mmodel));
		// continue from here

		for(int tri=0;tri<ourmodel->numberOfTriangles;tri++) {
			Triangle triangle_=ourmodel->triangles[tri];
			Vec3 *kenar1t=this->vertices[triangle_.getFirstVertexId()-1];
			Vec3 *kenar2t=this->vertices[triangle_.getSecondVertexId()-1];
			Vec3 *kenar3t=this->vertices[triangle_.getThirdVertexId()-1];
			Vec4 kenar1(kenar1t->x,kenar1t->y,kenar1t->z,1.0,kenar1t->colorId);
			Vec4 kenar2(kenar2t->x,kenar2t->y,kenar2t->z,1.0,kenar2t->colorId);
			Vec4 kenar3(kenar3t->x,kenar3t->y,kenar3t->z,1.0,kenar3t->colorId);
			Vec4 carpilmiskenar1t=multiplyMatrixWithVec4(MUpToVP,kenar1);
			Vec4 carpilmiskenar2t=multiplyMatrixWithVec4(MUpToVP,kenar2);
			Vec4 carpilmiskenar3t=multiplyMatrixWithVec4(MUpToVP,kenar3);
			carpilmiskenar1t.x/=carpilmiskenar1t.t;
			carpilmiskenar1t.y/=carpilmiskenar1t.t;
			carpilmiskenar1t.z/=carpilmiskenar1t.t;
			carpilmiskenar1t.t=1.0;
			carpilmiskenar2t.x/=carpilmiskenar2t.t;
			carpilmiskenar2t.y/=carpilmiskenar2t.t;
			carpilmiskenar2t.z/=carpilmiskenar2t.t;
			carpilmiskenar2t.t=1.0;
			carpilmiskenar3t.x/=carpilmiskenar3t.t;
			carpilmiskenar3t.y/=carpilmiskenar3t.t;
			carpilmiskenar3t.z/=carpilmiskenar3t.t;
			carpilmiskenar3t.t=1.0;
				if (this->cullingEnabled==1) 
				{
					Vec3 kenar0_cul(carpilmiskenar1t.x,carpilmiskenar1t.y,carpilmiskenar1t.z,carpilmiskenar1t.colorId);
					Vec3 kenar1_cul(carpilmiskenar2t.x,carpilmiskenar2t.y,carpilmiskenar2t.z,carpilmiskenar2t.colorId);
					Vec3 kenar2_cul(carpilmiskenar3t.x,carpilmiskenar3t.y,carpilmiskenar3t.z,carpilmiskenar3t.colorId);
					Vec3 N=crossProductVec3((subtractVec3(kenar1_cul,kenar0_cul)),(subtractVec3(kenar2_cul,kenar0_cul)));
					//normalize et.
					N=normalizeVec3(N);
					double control_res=dotProductVec3(kenar0_cul,N);
					if (control_res<0) continue;

				}


			if (ourmodel->type==0) {
				// DO CLIPPING
				Color* c0s[3];
				Color* c1s[3];
				for(int th=0;th<3;th++)
				{
					double x0;
					double x1;
					double y0;
					double y1;
					Color *c0;
					Color *c1;
					if(th==0)
					{
						x0 = carpilmiskenar1t.x;
						x1 = carpilmiskenar2t.x;
						y0 = carpilmiskenar1t.y;
						y1 = carpilmiskenar2t.y;
						c0s[0]=this->colorsOfVertices[carpilmiskenar1t.colorId-1];
						c1s[0]=this->colorsOfVertices[carpilmiskenar2t.colorId-1];
						c0=c0s[0];
						c1=c1s[0];
					}
					else if(th==1)
					{
						x0 = carpilmiskenar2t.x;
						y0 = carpilmiskenar2t.y;
						x1 = carpilmiskenar3t.x;
						y1 = carpilmiskenar3t.y;
						c0s[1]=this->colorsOfVertices[carpilmiskenar2t.colorId-1];
						c1s[1]=this->colorsOfVertices[carpilmiskenar3t.colorId-1];
						c0=c0s[1];
						c1=c1s[1];

					}
					else
					{
						x0 = carpilmiskenar3t.x;
						y0 = carpilmiskenar3t.y;
						x1 = carpilmiskenar1t.x;
						y1 = carpilmiskenar1t.y;
						c0s[2]=this->colorsOfVertices[carpilmiskenar3t.colorId-1];
						c1s[2]=this->colorsOfVertices[carpilmiskenar1t.colorId-1];		
						c0=c0s[2];
						c1=c1s[2];
					}

					double c1r = c1->r;
					double c1g = c1->g;
					double c1b = c1->b;
					double c0r = c0->r;
					double c0g = c0->g;
					double c0b = c0->b;	
					double te = 0;
					double tl = 1;
					bool visibility = false;
					double max = 1;
					double min = (-1);
					double dx = x1-x0;
					double dy = y1-y0;
					if (visible(dx,(min-x0),&te,&tl))
					{
						if (visible((-1)*dx,x0-max,&te,&tl))
						{
							if (visible(dy,min-y0,&te,&tl))
							{
								if (visible((-1)*dy,y0-max,&te,&tl))
								{
									visibility = true;
									if(tl<1)
									{
										//simdi eger x1 kesildiyse, color da degiscekk
										x1 = x0+dx*tl;
										y1 = y0+dy*tl;
										Color *tmc=new Color((c1r-c0r)*tl+c0r,(c1g-c0g)*tl+c0g,(c1b-c0b)*tl+c0b);
										c1s[th]=tmc;
									}
									if(te>0)
									{
										x0 = x0+dx*te;
										y0 = y0+dy*te;
										Color *tmc=new Color((c1r-c0r)*te+c0r,(c1g-c0g)*te+c0g,(c1b-c0b)*te+c0b);
										c0s[th]=tmc;
									}
								}
							}
						}
					}
					double z0,z1;
					if(th==0)
					{
						z0 = carpilmiskenar1t.z;
						z1 = carpilmiskenar2t.z;
					}
					else if(th==1)
					{
						z0 = carpilmiskenar2t.z;
						z1 = carpilmiskenar3t.z;
					}
					else if(th==0)
					{
						z0 = carpilmiskenar3t.z;
						z1 = carpilmiskenar1t.z;
					}
					//zye gerek var mı ki?
					drawLine(Mvp,x0,y0,z0,x1,y1,z1,*(c0s[th]),*(c1s[th]),nx,ny);
					
				}

			}

			else {
				Vec4 carpilmiskenar1=multiplyMatrixWithVec4(Mvp,carpilmiskenar1t);
				Vec4 carpilmiskenar2=multiplyMatrixWithVec4(Mvp,carpilmiskenar2t);
				Vec4 carpilmiskenar3=multiplyMatrixWithVec4(Mvp,carpilmiskenar3t);
				double xler[]={round(carpilmiskenar1.x),round(carpilmiskenar2.x),round(carpilmiskenar3.x)};
				double yler[]={round(carpilmiskenar1.y),round(carpilmiskenar2.y),round(carpilmiskenar3.y)};
				
				double max_xd=*(max_element(xler,xler+3));
				double min_xd=*(min_element(xler,xler+3));
				double max_yd=*(max_element(yler,yler+3));
				double min_yd=*(min_element(yler,yler+3));

				int xmin=int(round(min_xd));
				int xmax=int(round(max_xd));
				int ymin=int(round(min_yd));
				int ymax=int(round(max_yd));
				
				for(int yy=max(0, ymin);(yy<=ymax && yy<ny);yy++) {
					for (int xx = max(0,xmin); (xx <= xmax && xx<nx); xx++)
					{
						double alfa=(xx*(yler[1]-yler[2])+yy*(xler[2]-xler[1])+xler[1]*yler[2]-yler[1]*xler[2])/(xler[0]*(yler[1]-yler[2])+yler[0]*(xler[2]-xler[1])+xler[1]*yler[2]-yler[1]*xler[2]);
						double beta=(xx*(yler[2]-yler[0])+yy*(xler[0]-xler[2])+xler[2]*yler[0]-yler[2]*xler[0])/(xler[1]*(yler[2]-yler[0])+yler[1]*(xler[0]-xler[2])+xler[2]*yler[0]-yler[2]*xler[0]);
						double gama=(xx*(yler[0]-yler[1])+yy*(xler[1]-xler[0])+xler[0]*yler[1]-yler[0]*xler[1])/(xler[2]*(yler[0]-yler[1])+yler[2]*(xler[1]-xler[0])+xler[0]*yler[1]-yler[0]*xler[1]);

						if (alfa>=0 && beta>=0 && gama>=0) {

							Color *color1 = this->colorsOfVertices[carpilmiskenar1.colorId-1];
							Color *color2 = this->colorsOfVertices[carpilmiskenar2.colorId-1];
							Color *color3 = this->colorsOfVertices[carpilmiskenar3.colorId-1]; 
							Vec3 col1(color1->r,color1->g,color1->b,0);
							Vec3 col2(color2->r,color2->g,color2->b,0);
							Vec3 col3(color3->r,color3->g,color3->b,0);
							Vec3 col = addVec3(multiplyVec3WithScalar(col1,alfa),addVec3(multiplyVec3WithScalar(col2,beta),multiplyVec3WithScalar(col3,gama)));
							
							this->image[xx][yy].r=int(round(col.x));
							this->image[xx][yy].g=int(round(col.y));
							this->image[xx][yy].b=int(round(col.z));
						}
					}
				}

			}
			
		}
	}
}


/*
	Parses XML file
*/
Scene::Scene(const char *xmlPath)
{
	const char *str;
	XMLDocument xmlDoc;
	XMLElement *pElement;

	xmlDoc.LoadFile(xmlPath);

	XMLNode *pRoot = xmlDoc.FirstChild();

	// read background color
	pElement = pRoot->FirstChildElement("BackgroundColor");
	str = pElement->GetText();
	sscanf(str, "%lf %lf %lf", &backgroundColor.r, &backgroundColor.g, &backgroundColor.b);

	// read culling
	pElement = pRoot->FirstChildElement("Culling");
	if (pElement != NULL)
		pElement->QueryBoolText(&cullingEnabled);

	// read projection type
	pElement = pRoot->FirstChildElement("ProjectionType");
	if (pElement != NULL)
		pElement->QueryIntText(&projectionType);

	// read cameras
	pElement = pRoot->FirstChildElement("Cameras");
	XMLElement *pCamera = pElement->FirstChildElement("Camera");
	XMLElement *camElement;
	while (pCamera != NULL)
	{
		Camera *cam = new Camera();

		pCamera->QueryIntAttribute("id", &cam->cameraId);

		camElement = pCamera->FirstChildElement("Position");
		str = camElement->GetText();
		sscanf(str, "%lf %lf %lf", &cam->pos.x, &cam->pos.y, &cam->pos.z);

		camElement = pCamera->FirstChildElement("Gaze");
		str = camElement->GetText();
		sscanf(str, "%lf %lf %lf", &cam->gaze.x, &cam->gaze.y, &cam->gaze.z);

		camElement = pCamera->FirstChildElement("Up");
		str = camElement->GetText();
		sscanf(str, "%lf %lf %lf", &cam->v.x, &cam->v.y, &cam->v.z);

		cam->gaze = normalizeVec3(cam->gaze);
		cam->u = crossProductVec3(cam->gaze, cam->v);
		cam->u = normalizeVec3(cam->u);

		cam->w = inverseVec3(cam->gaze);
		cam->v = crossProductVec3(cam->u, cam->gaze);
		cam->v = normalizeVec3(cam->v);

		camElement = pCamera->FirstChildElement("ImagePlane");
		str = camElement->GetText();
		sscanf(str, "%lf %lf %lf %lf %lf %lf %d %d",
			   &cam->left, &cam->right, &cam->bottom, &cam->top,
			   &cam->near, &cam->far, &cam->horRes, &cam->verRes);

		camElement = pCamera->FirstChildElement("OutputName");
		str = camElement->GetText();
		cam->outputFileName = string(str);

		cameras.push_back(cam);

		pCamera = pCamera->NextSiblingElement("Camera");
	}

	// read vertices
	pElement = pRoot->FirstChildElement("Vertices");
	XMLElement *pVertex = pElement->FirstChildElement("Vertex");
	int vertexId = 1;

	while (pVertex != NULL)
	{
		Vec3 *vertex = new Vec3();
		Color *color = new Color();

		vertex->colorId = vertexId;

		str = pVertex->Attribute("position");
		sscanf(str, "%lf %lf %lf", &vertex->x, &vertex->y, &vertex->z);

		str = pVertex->Attribute("color");
		sscanf(str, "%lf %lf %lf", &color->r, &color->g, &color->b);

		vertices.push_back(vertex);
		colorsOfVertices.push_back(color);

		pVertex = pVertex->NextSiblingElement("Vertex");

		vertexId++;
	}

	// read translations
	pElement = pRoot->FirstChildElement("Translations");
	XMLElement *pTranslation = pElement->FirstChildElement("Translation");
	while (pTranslation != NULL)
	{
		Translation *translation = new Translation();

		pTranslation->QueryIntAttribute("id", &translation->translationId);

		str = pTranslation->Attribute("value");
		sscanf(str, "%lf %lf %lf", &translation->tx, &translation->ty, &translation->tz);

		translations.push_back(translation);

		pTranslation = pTranslation->NextSiblingElement("Translation");
	}

	// read scalings
	pElement = pRoot->FirstChildElement("Scalings");
	XMLElement *pScaling = pElement->FirstChildElement("Scaling");
	while (pScaling != NULL)
	{
		Scaling *scaling = new Scaling();

		pScaling->QueryIntAttribute("id", &scaling->scalingId);
		str = pScaling->Attribute("value");
		sscanf(str, "%lf %lf %lf", &scaling->sx, &scaling->sy, &scaling->sz);

		scalings.push_back(scaling);

		pScaling = pScaling->NextSiblingElement("Scaling");
	}

	// read rotations
	pElement = pRoot->FirstChildElement("Rotations");
	XMLElement *pRotation = pElement->FirstChildElement("Rotation");
	while (pRotation != NULL)
	{
		Rotation *rotation = new Rotation();

		pRotation->QueryIntAttribute("id", &rotation->rotationId);
		str = pRotation->Attribute("value");
		sscanf(str, "%lf %lf %lf %lf", &rotation->angle, &rotation->ux, &rotation->uy, &rotation->uz);

		rotations.push_back(rotation);

		pRotation = pRotation->NextSiblingElement("Rotation");
	}

	// read models
	pElement = pRoot->FirstChildElement("Models");

	XMLElement *pModel = pElement->FirstChildElement("Model");
	XMLElement *modelElement;
	while (pModel != NULL)
	{
		Model *model = new Model();

		pModel->QueryIntAttribute("id", &model->modelId);
		pModel->QueryIntAttribute("type", &model->type);

		// read model transformations
		XMLElement *pTransformations = pModel->FirstChildElement("Transformations");
		XMLElement *pTransformation = pTransformations->FirstChildElement("Transformation");

		pTransformations->QueryIntAttribute("count", &model->numberOfTransformations);

		while (pTransformation != NULL)
		{
			char transformationType;
			int transformationId;

			str = pTransformation->GetText();
			sscanf(str, "%c %d", &transformationType, &transformationId);

			model->transformationTypes.push_back(transformationType);
			model->transformationIds.push_back(transformationId);

			pTransformation = pTransformation->NextSiblingElement("Transformation");
		}

		// read model triangles
		XMLElement *pTriangles = pModel->FirstChildElement("Triangles");
		XMLElement *pTriangle = pTriangles->FirstChildElement("Triangle");

		pTriangles->QueryIntAttribute("count", &model->numberOfTriangles);

		while (pTriangle != NULL)
		{
			int v1, v2, v3;

			str = pTriangle->GetText();
			sscanf(str, "%d %d %d", &v1, &v2, &v3);

			model->triangles.push_back(Triangle(v1, v2, v3));

			pTriangle = pTriangle->NextSiblingElement("Triangle");
		}

		models.push_back(model);

		pModel = pModel->NextSiblingElement("Model");
	}
}

/*
	Initializes image with background color
*/
void Scene::initializeImage(Camera *camera)
{
	if (this->image.empty())
	{
		for (int i = 0; i < camera->horRes; i++)
		{
			vector<Color> rowOfColors;

			for (int j = 0; j < camera->verRes; j++)
			{
				rowOfColors.push_back(this->backgroundColor);
			}

			this->image.push_back(rowOfColors);
		}
	}
	// if image is filled before, just change color rgb values with the background color
	else
	{
		for (int i = 0; i < camera->horRes; i++)
		{
			for (int j = 0; j < camera->verRes; j++)
			{
				this->image[i][j].r = this->backgroundColor.r;
				this->image[i][j].g = this->backgroundColor.g;
				this->image[i][j].b = this->backgroundColor.b;
			}
		}
	}
}

/*
	If given value is less than 0, converts value to 0.
	If given value is more than 255, converts value to 255.
	Otherwise returns value itself.
*/
int Scene::makeBetweenZeroAnd255(double value)
{
	if (value >= 255.0)
		return 255;
	if (value <= 0.0)
		return 0;
	return (int)(value);
}

/*
	Writes contents of image (Color**) into a PPM file.
*/
void Scene::writeImageToPPMFile(Camera *camera)
{
	ofstream fout;

	fout.open(camera->outputFileName.c_str());

	fout << "P3" << endl;
	fout << "# " << camera->outputFileName << endl;
	fout << camera->horRes << " " << camera->verRes << endl;
	fout << "255" << endl;

	for (int j = camera->verRes - 1; j >= 0; j--)
	{
		for (int i = 0; i < camera->horRes; i++)
		{
			fout << makeBetweenZeroAnd255(this->image[i][j].r) << " "
				 << makeBetweenZeroAnd255(this->image[i][j].g) << " "
				 << makeBetweenZeroAnd255(this->image[i][j].b) << " ";
		}
		fout << endl;
	}
	fout.close();
}

/*
	Converts PPM image in given path to PNG file, by calling ImageMagick's 'convert' command.
	os_type == 1 		-> Ubuntu
	os_type == 2 		-> Windows
	os_type == other	-> No conversion
*/
void Scene::convertPPMToPNG(string ppmFileName, int osType)
{
	string command;

	// call command on Ubuntu
	if (osType == 1)
	{
		command = "convert " + ppmFileName + " " + ppmFileName + ".png";
		system(command.c_str());
	}

	// call command on Windows
	else if (osType == 2)
	{
		command = "magick convert " + ppmFileName + " " + ppmFileName + ".png";
		system(command.c_str());
	}

	// default action - don't do conversion
	else
	{
	}
}