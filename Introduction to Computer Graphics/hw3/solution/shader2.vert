#version 410

layout(location = 0) in vec3 position;

// Data from CPU
uniform mat4 MVP; // ModelViewProjection Matrix
uniform mat4 MV; // ModelView idMVPMatrix
uniform vec4 cameraPosition;
uniform vec3 lightPosition;
uniform float heightFactor;
uniform int leftrightamount;

// Texture-related data
uniform sampler2D tex0;
uniform sampler2D tex1;
uniform int widthTexture;
uniform int heightTexture;

// Output to Fragment Shader
out vec2 textureCoordinate; // For texture-color
out vec3 vertexNormal; // For Lighting computation
out vec3 ToLightVector; // Vector from Vertex to Light;
out vec3 ToCameraVector; // Vector from Vertex to Camera;

void main()
{

    // get texture value, compute height
    vec3 pos = position;

    float alpha=(3.1415926535897932384626433832795*2)*(position.x/widthTexture);
    float beta=(3.1415926535897932384626433832795)*(position.z/heightTexture);

    textureCoordinate=vec2((position.x+leftrightamount)/widthTexture,position.z/heightTexture);
    vec3 heightColor=texture(tex1,textureCoordinate).xyz;

    pos.x=350*sin(beta)*cos(alpha);
    pos.y=350*sin(beta)*sin(alpha)+heightFactor*heightColor.x;
    pos.z=350*cos(beta);


    // compute normal vector using also the heights of neighbor vertices
    vec2 nTC=vec2(((position.x+leftrightamount)-1)/widthTexture,position.z/heightTexture);
    vec3 hC=texture(tex1,nTC).xyz;
    vec3 n1=vec3(position.x-1,heightFactor*hC.x,position.z);
    alpha=(6.28)*((position.x-1)/widthTexture);
    beta=(3.14)*(position.z/heightTexture);
    n1.x=350*sin(beta)*cos(alpha);
    n1.y=350*sin(beta)*sin(alpha)+heightFactor*hC.x;
    n1.z=350*cos(beta);
    n1=n1-pos;

    nTC=vec2(((position.x+leftrightamount)-1)/widthTexture,(position.z+1)/heightTexture);
    hC=texture(tex1,nTC).xyz;
    vec3 n2=vec3(position.x-1,heightFactor*hC.x,position.z+1);
    alpha=(6.28)*((position.x-1)/widthTexture);
    beta=(3.14)*((position.z+1)/heightTexture);
    n2.x=350*sin(beta)*cos(alpha);
    n2.y=350*sin(beta)*sin(alpha)+heightFactor*hC.x;
    n2.z=350*cos(beta);
    n2=n2-pos;
    
    nTC=vec2(((position.x+leftrightamount))/widthTexture,(position.z+1)/heightTexture);
    hC=texture(tex1,nTC).xyz;
    vec3 n3=vec3(position.x-1,heightFactor*hC.x,position.z+1);
    alpha=(6.28)*((position.x)/widthTexture);
    beta=(3.14)*((position.z+1)/heightTexture);
    n3.x=350*sin(beta)*cos(alpha);
    n3.y=350*sin(beta)*sin(alpha)+heightFactor*hC.x;
    n3.z=350*cos(beta);
    n3=n3-pos;

    nTC=vec2(((position.x+leftrightamount)+1)/widthTexture,(position.z)/heightTexture);
    hC=texture(tex1,nTC).xyz;
    vec3 n4=vec3(position.x-1,heightFactor*hC.x,position.z+1);
    alpha=(6.28)*((position.x+1)/widthTexture);
    beta=(3.14)*((position.z)/heightTexture);
    n4.x=350*sin(beta)*cos(alpha);
    n4.y=350*sin(beta)*sin(alpha)+heightFactor*hC.x;
    n4.z=350*cos(beta);
    n4=n4-pos;

    nTC=vec2(((position.x+leftrightamount)+1)/widthTexture,(position.z-1)/heightTexture);
    hC=texture(tex1,nTC).xyz;
    vec3 n5=vec3(position.x-1,heightFactor*hC.x,position.z+1);
    alpha=(6.28)*((position.x+1)/widthTexture);
    beta=(3.14)*((position.z-1)/heightTexture);
    n5.x=350*sin(beta)*cos(alpha);
    n5.y=350*sin(beta)*sin(alpha)+heightFactor*hC.x;
    n5.z=350*cos(beta);
    n5=n5-pos;

    nTC=vec2(((position.x+leftrightamount))/widthTexture,(position.z-1)/heightTexture);
    hC=texture(tex1,nTC).xyz;
    vec3 n6=vec3(position.x-1,heightFactor*hC.x,position.z+1);
    alpha=(6.28)*((position.x)/widthTexture);
    beta=(3.14)*((position.z-1)/heightTexture);
    n6.x=350*sin(beta)*cos(alpha);
    n6.y=350*sin(beta)*sin(alpha)+heightFactor*hC.x;
    n6.z=350*cos(beta);
    n6=n6-pos;



       vertexNormal = normalize(cross(n1, n2) + cross(n2, n3) + cross(n3, n4) + cross(n4, n5)
                            + cross(n5, n6) + cross(n6, n1));



    ToLightVector = normalize(lightPosition - pos);

 ToCameraVector = normalize(cameraPosition.xyz - pos);

    gl_Position = MVP * vec4(pos.x/2,pos.y/2,pos.z/2, 1.0);

}
