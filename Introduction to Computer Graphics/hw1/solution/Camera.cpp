#include "Camera.h"
#include <string.h>
#include<iostream>
#include<cmath>
using namespace std;
Camera::Camera(int id,                      // Id of the camera
               const char* imageName,       // Name of the output PPM file 
               const Vector3f& pos,         // Camera position
               const Vector3f& gaze,        // Camera gaze direction
               const Vector3f& up,          // Camera up direction
               const ImagePlane& imgPlane)  // Image plane parameters
{
	/***********************************************
     *                                             *
	 * TODO: Implement this function               *
     *                                             *
     ***********************************************
	 */
	this->id=id;
	strcpy(this->imageName,imageName);
	this->pos=pos;
	this->gaze=gaze;
	this->imgPlane=imgPlane;
	this->up=up;
}

/* Takes coordinate of an image pixel as row and col, and
 * returns the ray going through that pixel. 
 */
Ray Camera::getPrimaryRay(int col, int row) const
{
	Vector3f u=cross_product(up,scalar_product(gaze,-1));
	Vector3f m=sum(pos,scalar_product(gaze,imgPlane.distance));

	
	Vector3f q=sum(m,sum(scalar_product(u,imgPlane.left),scalar_product(up,imgPlane.top)));
	float su=(col+0.5)*((imgPlane.right-imgPlane.left)/imgPlane.nx);
	float sv=(row+0.5)*((imgPlane.top-imgPlane.bottom)/imgPlane.ny);

	Vector3f s=sum(q,sub(scalar_product(u,su),scalar_product(up,sv)));

	Ray ray;
	ray.origin=pos;
	ray.direction.x=sub(s,pos).x/sqrt(dot_product(sub(s,pos),sub(s,pos)));
	ray.direction.y=sub(s,pos).y/sqrt(dot_product(sub(s,pos),sub(s,pos)));
	ray.direction.z=sub(s,pos).z/sqrt(dot_product(sub(s,pos),sub(s,pos)));

	return ray;
	/***********************************************
     *                                             *
	 * TODO: Implement this function               *
     *                                             *
     ***********************************************
	 */
}

