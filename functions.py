import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from random import random
plt.style.use('seaborn-pastel')

N = 60 # número de puntos en cada dirección

x_start, x_end = -2.0, 2.0 # límites en dirección x
y_start, y_end = -2.0, 2.0 # límite en dirección y

x = np.linspace(x_start, x_end, N) # crea arreglo de 1D con coord X
y = np.linspace(y_start, y_end, N) # crea arreglo de 1D con coord Y

X, Y = np.meshgrid(x,y) # genera una mesh grid (grilla de puntos)

""" Flujo uniforme en X """
def potential_uniformX(U, x, y):
  return U * x

def stream_uniformX(U, x, y):
  return U * y
  
def velocity_uniformX(U):
  return (U * np.ones((N, N), dtype=float), 0 * np.ones((N, N), dtype=float))

def pressure_uniformX(U):
    u, v = velocity_uniformX(U)
    return 1.0 - (u**2 + v**2) / U**2


""" Flujo uniforme en Y """

def potential_uniformY(U, x, y):
  return U * y

def stream_uniformY(U, x, y):
  return U * x

def velocity_uniformY(U):
  return (0 * np.ones((N, N), dtype=float), U * np.ones((N, N), dtype=float))

def pressure_uniformY(U):
    u, v = velocity_uniformY(U)
    return 1.0 - (u**2 + v**2) / U**2


""" Flujo uniforme en a = alpha """

def potential_uniformDiag(U, alfa, x, y):
  return U * (x * np.cos(alfa) + y * np.sin(alfa))

def stream_uniformDiag(U, alfa, x, y):
  return U * (y * np.cos(alfa) - x * np.sin(alfa))

def velocity_uniformDiag(U, alfa):
  return (U * np.cos(alfa) * np.ones( (N, N), dtype=float ), U * np.sin(alfa) * np.ones( (N, N), dtype=float ))

def pressure_uniformDiag(U, alfa):
    u, v = velocity_uniformDiag(U, alfa)
    return 1.0 - (u**2 + v**2) / U**2

""" Fuente o sumidero """

def potential_SourceSink(M, xs, ys):
  return M * np.log(np.sqrt((X-xs)**2 + (Y-ys)**2))

def stream_SourceSink(M, xs, ys):
  return M  * np.arctan2((Y-ys), (X-xs))

def velocity_SourceSink(M, xs, ys):
  return (M  * (X-xs) / ((X-xs)**2 + (Y-ys)**2), M * (Y-ys) / ((X-xs)**2 + (Y-ys)**2))

def pressure_SourceSink(M, xs, ys, inf):
    u, v = velocity_SourceSink(M, xs, ys)
    return 1.0 - (u**2 + v**2) / inf**2


""" Vortex """

def potential_Vortex(gamma, xv, yv):
  return gamma * np.arctan((Y-yv)**2,(X-xv)**2)

def stream_Vortex(gamma, xv, yv):
  return gamma * np.log(np.sqrt((X-xv)**2 + (Y-yv)**2))

def velocity_Vortex(gamma, xv, yv):
  return (2*gamma * (Y-yv) / ((X-xv)**2 + (Y-yv)**2), -2*gamma * (X-xv) / ((X-xv)**2 + (Y-yv)**2))

def pressure_Vortex(gamma, xv, yv, inf): # REVISAR REVISAR REVISAR
    u, v = velocity_Vortex(gamma, xv, yv)
    return 1.0 - (u**2 + v**2) / inf**2


def superposicion(u_list, v_list, psi_list, potencia, corriente, presion):

  #Superposición
  u = np.zeros((N, N))
  for elem in u_list:
    u += elem
  v = np.zeros((N, N))
  for elem in v_list:
    v += elem
  psi = np.zeros((N, N))
  for elem in psi_list:
    psi += elem

  #Graficamos
  
  fig, ax = plt.subplots()
  plt.xlim(-2, 2)
  plt.ylim(-2, 2)

  if corriente:
    plt.streamplot(X, Y, u, v, density=1, linewidth=1, arrowsize=1, arrowstyle='->', color="brown") 
  if potencia:
    plt.streamplot(X, Y, -v, u, density=1, linewidth=1, arrowsize=1, arrowstyle='-', color="gray") 
  if presion:
    cp = 1.0 - (u**2 + v**2) / 1**2
    contf = plt.contourf(X, Y, cp, levels=np.linspace(-2, 2, 100), extend='both')
    cbar = plt.colorbar(contf)
    cbar.set_label('C_p', fontsize=16)
    cbar.set_ticks([-2, -2, -2, 2])

  scats = []


  xline = [random()*4 - 2 for _ in range(200)]
  yline = [random()*4 - 2 for _ in range(200)]

  # animation function.  This is called sequentially
  def animate(i):
      if scats:
          scats[0].remove()
          scats.pop(0)

      delx = []
      dely = []
      for i in range(len(xline)):
        if not 0 <= round((xline[i] + 2) * 15) < 59 or not 0 <= round((yline[i] + 2) * 15) < 59:
          delx.append(xline[i])
          dely.append(yline[i])
        else:
          x_index_in_velocity = int((xline[i] + 2) * 15)
          y_index_in_velocity = int((yline[i] + 2) * 15)


          vel_x = u[y_index_in_velocity][x_index_in_velocity]
          vel_y = v[y_index_in_velocity][x_index_in_velocity]

          xline[i] += vel_x/30
          yline[i] += vel_y/30

      scat = plt.scatter([x for x in xline if not x in delx], [y for y in yline if not y in dely], color="orange", s=8)
      scats.append(scat)
      
      return scat,

  anim = animation.FuncAnimation(fig, animate, frames=15, interval=100, repeat=True)
  anim.save('static/img/line.gif', writer='imagemagick')
  
  return fig