from functions import superposicion
from functions import velocity_SourceSink, velocity_uniformDiag, velocity_uniformX, velocity_uniformY, velocity_Vortex
from functions import stream_SourceSink, stream_uniformDiag, stream_uniformX, stream_uniformY, stream_Vortex
from functions import vel_inf_A, vel_inf_SS, vel_inf_V, vel_inf_X, vel_inf_Y
import numpy as np

def graph(params, what, potencia, corriente, presion, puntos):
    """
        [(U), (U), (U, alpha), (M, x, y), (M, x, y), (gamma, x, y)], [Boolean, Boolean, Boolean, Boolean, Boolean, Boolean]
    """

    U_x = params[0][0]
    U_y = params[1][0]

    U_diag, alpha = params[2]
    alpha = alpha * np.pi

    M_sink, x_sink, y_sink = params[4]
    M_sink = -M_sink
    M_source, x_source, y_source = params[3]
    gamma, xv, yv = params[5]

    N = 60 # número de puntos en cada dirección

    x_start, x_end = -20, 20 # límites en dirección x
    y_start, y_end = -10, 10 # límite en dirección y

    x = np.linspace(x_start, x_end, N) # crea arreglo de 1D con coord X
    y = np.linspace(y_start, y_end, N) # crea arreglo de 1D con coord Y

    X, Y = np.meshgrid(x,y) # genera una mesh grid (grilla de puntos)

    # Vortex
    u_vortex, v_vortex = velocity_Vortex(gamma, xv, yv)
    psi_vortex = stream_Vortex(gamma, xv, yv)
    inf_vortex = vel_inf_V(gamma, xv, yv)

    # Sink
    
    u_sink, v_sink = velocity_SourceSink(M_sink, x_sink, y_sink)
    psi_sink = stream_SourceSink(M_sink, x_sink, y_sink)
    inf_sink = vel_inf_SS(M_sink, x_sink, y_sink)

    # Source
    u_source, v_source = velocity_SourceSink(M_source, x_source, y_source)
    psi_source = stream_SourceSink(M_source, x_source, y_source)
    inf_source = vel_inf_SS(M_source, x_source, y_source)

    # Uniform X
    u_x, v_x = velocity_uniformX(U_x)
    psi_uniform_X = stream_uniformX(U_x, X, Y)
    inf_x = U_x

    # Uniform Y
    u_y, v_y = velocity_uniformY(U_y)
    psi_uniform_Y = stream_uniformX(U_y, X, Y)
    inf_y = U_y

    # Uniform Alpha
    u_diag, v_diag = velocity_uniformDiag(U_diag, alpha)
    psi_diag = stream_uniformDiag(U_diag, alpha, X, Y)
    inf_a = U_diag

    inf_list = [inf_x, inf_y, inf_a, inf_source, inf_sink, inf_vortex]
    u_list = [u_x, u_y, u_diag, u_source, u_sink, u_vortex]
    v_list = [v_x, v_y, v_diag, v_source, v_sink, v_vortex]
    psi_list = [psi_uniform_X, psi_uniform_Y, psi_diag, psi_source, psi_sink, psi_vortex]

    def get_boolean(index):
        return what[index]

    new_ulist = []
    new_vlist = []
    new_psilist = []
    new_inf = 0
    for i in range(len(u_list)):
        if get_boolean(i):
            new_ulist.append(u_list[i])
            new_vlist.append(v_list[i])
            new_psilist.append(psi_list[i])
            new_inf += inf_list[i]


    return superposicion(new_ulist, new_vlist, new_psilist, new_inf, potencia, corriente, presion, puntos)





