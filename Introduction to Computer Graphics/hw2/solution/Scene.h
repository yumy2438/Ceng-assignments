#ifndef _SCENE_H_
#define _SCENE_H_

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <iostream>
#include <string>
#include <vector>

#include "Camera.h"
#include "Color.h"
#include "Model.h"
#include "Rotation.h"
#include "Scaling.h"
#include "Helpers.h"
#include "Translation.h"
#include "Triangle.h"
#include "Vec3.h"
#include "Vec4.h"

using namespace std;

class Scene
{
public:
	Color backgroundColor;
	bool cullingEnabled;
	int projectionType;

	vector< vector<Color> > image;
	vector< Camera* > cameras;
	vector< Vec3* > vertices;
	vector< Color* > colorsOfVertices;
	vector< Scaling* > scalings;
	vector< Rotation* > rotations;
	vector< Translation* > translations;
	vector< Model* > models;

	Scene(const char *xmlPath);

	void initializeImage(Camera* camera);
	void forwardRenderingPipeline(Camera* camera);
	int makeBetweenZeroAnd255(double value);
	void writeImageToPPMFile(Camera* camera);
	void convertPPMToPNG(string ppmFileName, int osType);
	Color calculateColor(Color *c0,Color *c1,int x,int y,int x0,int y0,int x1,int y1,double m);
	void setPixel(int x,int y,Color c,int nx,int ny);
	double calculatef(int x,int y,int x0,int y0,int x1,int y1);
	bool visible(double den,double num,double *te,double *tl);
	void drawLine(Matrix4 Mvp,double x0_bef,double y0_bef,double z0_bef,double x1_bef,double y1_bef,double z1_bef,Color c0,Color c1,int nx,int ny);

};

#endif