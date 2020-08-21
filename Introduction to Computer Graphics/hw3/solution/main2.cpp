#include "helper2.h"
#include "glm/glm.hpp"
#include "glm/gtc/matrix_inverse.hpp"
#include "glm/gtx/rotate_vector.hpp"

static GLFWwindow * win = NULL;


// Shaders
GLuint idProgramShader;
GLuint idFragmentShader;
GLuint idVertexShader;
GLuint idMVPMatrix;
int widthTexture, heightTexture, leftrightamount, lightY=1600, lightX=0, lightZ=0;

GLfloat heightFactor = 0.0f;
GLfloat speed=0.0f;

glm::mat4 proj_matr = glm::perspective(45.0, 1.0, 0.1, 1000.0);

glm::vec3 cam_pos = glm::vec3(0, 600, 0);

glm::vec3 cam_gaze = glm::vec3(0.0, -1.0, 0.0);

glm::vec3 center = glm::vec3(0.0,0.0,0.0);

glm::vec3 cam_up = glm::vec3(0.0, 0.0, 1.0);

glm::vec3 cam_cross = cross(cam_up,cam_gaze);


static void key_callback(GLFWwindow* window, int key, int scancode, int action, int mods)
{
    if (key == GLFW_KEY_Q)
        leftrightamount-=1;
    else if (key == GLFW_KEY_E)
          leftrightamount+=1;
    else if (key == GLFW_KEY_F)
        heightFactor-=1;
    else if (key == GLFW_KEY_R)
          heightFactor+=1;
    else if (key == GLFW_KEY_G)
        lightY-=5;
    else if (key == GLFW_KEY_T)
        lightY+=5;
    else if (key == GLFW_KEY_LEFT)
        lightX-=5;
    else if (key == GLFW_KEY_RIGHT)
        lightX+=5;
    else if (key == GLFW_KEY_UP)
        lightZ+=5;
    else if (key == GLFW_KEY_DOWN)
        lightZ-=5;
    else if (key == GLFW_KEY_Y && action == GLFW_PRESS)
        speed+=0.01;
    else if (key == GLFW_KEY_H && action == GLFW_PRESS)
        speed-=0.01;
    else if (key == GLFW_KEY_X && action == GLFW_PRESS)
        speed=0.0;
    else if (key == GLFW_KEY_I && action == GLFW_PRESS) {
    	speed=0.0;

		cam_pos = glm::vec3(0, 600, 0);

		cam_gaze = glm::vec3(0.0, -1.0, 0.0);

		center = glm::vec3(0.0,0.0,0.0);

		cam_up = glm::vec3(0.0, 0.0, 1.0);

		cam_cross = cross(cam_up,cam_gaze);

    }
  else if(key == GLFW_KEY_W )
  {
    cam_up = glm::rotate(cam_up, 0.05f, cam_cross);
    cam_gaze = glm::rotate(cam_gaze, 0.05f, cam_cross);
  }
  else if(key == GLFW_KEY_S )
  {
    cam_up = glm::rotate(cam_up, -0.05f, cam_cross);
    cam_gaze = glm::rotate(cam_gaze, -0.05f, cam_cross);
  }
  //yaw -> up
  else if(key == GLFW_KEY_A)
  {
    cam_gaze = glm::rotate(cam_gaze, 0.05f, cam_up);
  }
  else if(key == GLFW_KEY_D)
  {
    cam_gaze = glm::rotate(cam_gaze, -0.05f, cam_up);
  }
}



static void errorCallback(int error,
  const char * description) {
  fprintf(stderr, "Error: %s\n", description);
}

int main(int argc, char * argv[]) {

  if (argc != 3) {
    printf("Two texture image expected!\n");
    exit(-1);
  }

  glfwSetErrorCallback(errorCallback);

  if (!glfwInit()) {
    exit(-1);
  }

  glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
  glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 2);
  glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_COMPAT_PROFILE);


  win = glfwCreateWindow(1000, 1000, "CENG477 - HW3", NULL, NULL);

  if (!win) {
    glfwTerminate();
    exit(-1);
  }
  glfwMakeContextCurrent(win);

  GLenum err = glewInit();
  if (err != GLEW_OK) {
    fprintf(stderr, "Error: %s\n", glewGetErrorString(err));

    glfwTerminate();
    exit(-1);
  }

  initShaders();
  glUseProgram(idProgramShader);
  initTexture(argv[2], & widthTexture, & heightTexture);
  initTexture2(argv[1], & widthTexture, & heightTexture);
glfwSetKeyCallback(win, key_callback);
  /***************************************************************************/
widthTexture=125;
heightTexture=	250;
    int vertex_cnt = 6 * widthTexture * heightTexture;
    glm::vec3* vertices = new glm::vec3[vertex_cnt];
    int index=0;
    for(int i = 0; i < widthTexture; i++){
        for(int j = 0; j < heightTexture; j++){



            glm::vec3 v0= glm::vec3(i, 0, j);

            glm::vec3 v1=glm::vec3(i+1, 0, j+1);

            glm::vec3 v2=glm::vec3(i+1, 0, j);

            glm::vec3 v3= glm::vec3(i, 0, j+1);

            vertices[index++]=v0;
            vertices[index++]=v1;
            vertices[index++]=v2;
            vertices[index++]=v3;
            vertices[index++]=v0;
            vertices[index++]=v1;
        }
    }


    glUniform1i(glGetUniformLocation(idProgramShader, "widthTexture"), widthTexture);

    glUniform1i(glGetUniformLocation(idProgramShader, "heightTexture"), heightTexture);


leftrightamount=0;

  glEnable(GL_DEPTH_TEST);

  while (!glfwWindowShouldClose(win)) {
int width,height;
  	glfwGetWindowSize(win,&width, &height);
glViewport(0,0,width,height);


cam_pos += speed * cam_gaze;
      cam_cross = cross(cam_up,cam_gaze);

       glm::vec3 center = cam_pos + cam_gaze * 0.1f;

      glm::mat4 view_matr = glm::lookAt(cam_pos, center, cam_up);


      glm::mat4 mvp_matr = proj_matr * view_matr ;

      glm::mat4  norm_matr = glm::inverseTranspose(view_matr);


    glUniformMatrix4fv(glGetUniformLocation(idProgramShader, "MV"), 1, GL_FALSE, &view_matr[0][0]);

    glUniformMatrix4fv(glGetUniformLocation(idProgramShader, "MVP"), 1, GL_FALSE, &mvp_matr[0][0]);

    glUniformMatrix4fv(glGetUniformLocation(idProgramShader, "M_norm"), 1, GL_FALSE, &norm_matr[0][0]);

    glUniform3fv(glGetUniformLocation(idProgramShader, "cameraPosition"), 1, &cam_pos[0]);


      GLint loc_sampler = glGetUniformLocation(idProgramShader, "tex0");
    glUniform1i(loc_sampler, 0);

         GLint loc_sampler2 = glGetUniformLocation(idProgramShader, "tex1");
    glUniform1i(loc_sampler2, 1);



    glUniform1i(glGetUniformLocation(idProgramShader, "leftrightamount"), leftrightamount);
    glUniform1f(glGetUniformLocation(idProgramShader, "heightFactor"), heightFactor);

    glm::vec3 light_pos=glm::vec3(lightX,lightY,lightZ);
    glUniform3fv(glGetUniformLocation(idProgramShader, "lightPosition"), 1, &light_pos[0]);

    glClearStencil(0);
    glClearDepth(1.0f);
    glClearColor(0, 0, 0, 1);
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT);
    
    glEnableClientState(GL_VERTEX_ARRAY);
    glVertexPointer(3, GL_FLOAT, 0, vertices);
    glDrawArrays(GL_TRIANGLES, 0, vertex_cnt);
    glDisableClientState(GL_VERTEX_ARRAY);

      glfwSwapBuffers(win);
      glfwPollEvents();
  }

  /***************************************************************************/
  glfwDestroyWindow(win);
  glfwTerminate();

  return 0;
}
