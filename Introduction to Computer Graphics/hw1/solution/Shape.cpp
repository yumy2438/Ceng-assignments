#include "Shape.h"
#include "Scene.h"
#include <cmath>
#include <limits>
Shape::Shape(void)
{
}

Shape::Shape(int id, int matIndex)
    : id(id), matIndex(matIndex)
{
}

Sphere::Sphere(void)
{}

/* Constructor for sphere. You will implement this. */
Sphere::Sphere(int id, int matIndex, int cIndex, float R, vector<Vector3f> *pVertices)
    : Shape(id, matIndex)
{
	this->center=pVertices->at(cIndex-1);
	this->R=R;
	/***********************************************
     *                                             *
	 * TODO: Implement this function               *
     *                                             *
     ***********************************************
	 */
}

/* Sphere-ray intersection routine. You will implement this. 
Note that ReturnVal structure should hold the information related to the intersection point, e.g., coordinate of that point, normal at that point etc. 
You should to declare the variables in ReturnVal structure you think you will need. It is in defs.h file. */
ReturnVal Sphere::intersect(const Ray & ray) const
{
	ReturnVal ret;
	Vector3f ray_direction = ray.direction;
	Vector3f ray_origin = ray.origin;
	float this_R = this->R;
	Vector3f this_center = this->center;
	float a=dot_product(ray_direction,ray_direction);
	Vector3f omc=sub(ray_origin,this_center);
	float b=dot_product(ray_direction,omc)*2;
	float c=dot_product(omc,omc)-this_R*this_R;

	float disc=b*b-4*a*c;
	if(disc<0) {
		ret.is_intersected=false;
		ret.t=-1;
		return ret;
	}
	float t1=(-1*b-sqrt(disc))/2*a;
	float t2=(-1*b+sqrt(disc))/2*a;
	if(t1<0 && t2<0) {
		ret.is_intersected=false;
	ret.t=-1;
		return ret;
	}
	if(t1<t2) {
		if(t1<0) {
			ret.t=t2;
		}
		else {
			ret.t=t1;
		}
	}
	else if(t2<t1) {
		if(t2<0) {
			ret.t=t1;
		}
		else {
			ret.t=t2;
		}
	}
	ret.intersection_point=sum(ray_origin,scalar_product(ray_direction,ret.t));
	Vector3f for_normal=sub(ret.intersection_point,this_center);
	ret.surface_normal.x=for_normal.x/this_R;
	ret.surface_normal.y=for_normal.y/this_R;
	ret.surface_normal.z=for_normal.z/this_R;
	ret.is_intersected=true;
	return ret;
	/***********************************************
     *                                             *
	 * TODO: Implement this function               *
     *                                             *
     ***********************************************
	 */
}

Triangle::Triangle(void)
{}

/* Constructor for triangle. You will implement this. */
Triangle::Triangle(int id, int matIndex, int p1Index, int p2Index, int p3Index, vector<Vector3f> *pVertices)
    : Shape(id, matIndex)
{
	this->a=pVertices->at(p1Index-1);
	this->b=pVertices->at(p2Index-1);
	this->c=pVertices->at(p3Index-1);
	/***********************************************
     *                                             *
	 * TODO: Implement this function               *
     *                                             *
     ***********************************************
	 */
}

/* Triangle-ray intersection routine. You will implement this. 
Note that ReturnVal structure should hold the information related to the intersection point, e.g., coordinate of that point, normal at that point etc. 
You should to declare the variables in ReturnVal structure you think you will need. It is in defs.h file. */
ReturnVal Triangle::intersect(const Ray & ray) const
{
	Vector3f this_a = this->a;
	Vector3f this_b = this->b;
	Vector3f this_c = this->c;
	Vector3f ray_origin = ray.origin;
	Vector3f ray_direction = ray.direction;
	Vector3f thisa_thisb = sub(this_a,this_b);
	Vector3f thisa_thisc = sub(this_a,this_c);
	Vector3f thisa_rayo = sub(this_a,ray_origin);
	float A=det(thisa_thisb,thisa_thisc,ray_direction);
	float det_beta=det(thisa_rayo,thisa_thisc,ray_direction);
	float det_gama=det(thisa_thisb,thisa_rayo,ray_direction);
	float det_t=det(thisa_thisb,thisa_thisc,thisa_rayo);

	float beta=det_beta/A;
	float gama=det_gama/A;
	float t=det_t/A;
	float epsi=pScene->intTestEps*-1;
	if(t>=0 && (beta+gama+2*epsi)<=(1) && beta>=epsi && gama>=epsi) {
		ReturnVal ret;
		ret.t=t;
		ret.is_intersected=true;
		ret.intersection_point=sum(ray_origin,scalar_product(ray_direction,t));
		Vector3f surface_normal=cross_product(sub(b,a),sub(c,a));
		float dd=sqrt(dot_product(surface_normal,surface_normal));
		surface_normal.x=surface_normal.x/dd;
		surface_normal.y=surface_normal.y/dd;
		surface_normal.z=surface_normal.z/dd;
		ret.surface_normal=surface_normal;
		return ret;
	}
	ReturnVal ret;
	ret.is_intersected=false;
	ret.t=-1;
	return ret;
	/***********************************************
     *                                             *
	 * TODO: Implement this function               *
     *                                             *
     ***********************************************
	 */
}

Mesh::Mesh()
{}

/* Constructor for mesh. You will implement this. */
Mesh::Mesh(int id, int matIndex, const vector<Triangle>& faces, vector<int> *pIndices, vector<Vector3f> *pVertices)
    : Shape(id, matIndex)
{
	for (int i=0; i<faces.size(); i++) 
        (this->faces).push_back(faces[i]);
	/***********************************************
     *                                             *
	 * TODO: Implement this function               *
     *                                             *
     ***********************************************
	 */
}

/* Mesh-ray intersection routine. You will implement this. 
Note that ReturnVal structure should hold the information related to the intersection point, e.g., coordinate of that point, normal at that point etc. 
You should to declare the variables in ReturnVal structure you think you will need. It is in defs.h file. */
ReturnVal Mesh::intersect(const Ray & ray) const
{
	bool is_intersect=0;
	float tt=std::numeric_limits<std::int32_t>::max();
	Vector3f s_normal;
	for (int i=0; i<faces.size(); i++) {
		ReturnVal r=faces[i].intersect(ray);
		float r_t = r.t;
		if(r.is_intersected && r_t<=tt) {
			is_intersect=true;
			s_normal=r.surface_normal;
			tt=r_t;
		}
	}
	if(is_intersect) {
		ReturnVal ret;
		ret.t=tt;
		ret.is_intersected=true;
		ret.intersection_point=sum(ray.origin,scalar_product(ray.direction,tt));
		ret.surface_normal=s_normal;
		return ret;
	}
	ReturnVal ret;
	ret.t=-1;
	ret.is_intersected=false;
	return ret;
	/***********************************************
     *                                             *
	 * TODO: Implement this function               *
     *                                             *
     ***********************************************
	 */
}
