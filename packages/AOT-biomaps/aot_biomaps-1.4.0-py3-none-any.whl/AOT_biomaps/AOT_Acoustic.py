import scipy.io
import numpy as np
import h5py
from scipy.signal import hilbert
from math import ceil, sin, cos, radians, floor
import os
from kwave.kgrid import kWaveGrid
from kwave.kmedium import kWaveMedium
from kwave.ksource import kSource
from kwave.ksensor import kSensor
from kwave.kspaceFirstOrder3D import kspaceFirstOrder3D
from kwave.kspaceFirstOrder2D import kspaceFirstOrder2D
from kwave.utils.signals import tone_burst
from kwave.options.simulation_options import SimulationOptions
from kwave.options.simulation_execution_options import SimulationExecutionOptions
import matplotlib.pyplot as plt
import GPUtil
from tempfile import gettempdir
if AOT_biomaps.__process__ == 'gpu':
    import cupy as cp
    from cupyx.scipy.signal import hilbert as cp_hilbert
else:
    import numpy as cp
    from scipy.signal import hilbert as cp_hilbert


def select_best_gpu():
    try:
        # Obtenez la liste des GPU disponibles
        gpus = GPUtil.getGPUs()
        if not gpus:
            print("Aucun GPU disponible.")
            return [False, None]

        best_gpu = 0
        max_memory = 0

        for i, gpu in enumerate(gpus):
            # Obtenez la mémoire totale et utilisée pour chaque GPU
            total_memory = gpu.memoryTotal
            used_memory = gpu.memoryUsed
            available_memory = total_memory - used_memory

            # Sélectionnez le GPU avec le plus de mémoire disponible
            if available_memory > max_memory:
                max_memory = available_memory
                best_gpu = i

        print(f"Le meilleur GPU est GPU {best_gpu} avec {max_memory:.2f} MB disponibles.")
        return [True, best_gpu]

    except Exception as e:
        print(f"Erreur lors de la sélection du GPU : {e}")
        return [False, None]


def hex_to_binary_array(hex_string):
    # Convertir chaque caractère hexadécimal en 4 bits binaires
    binary_string = ''.join(f"{int(char, 16):04b}" for char in hex_string)
    # Convertir la chaîne binaire en un tableau NumPy de 0 et 1
    return np.array(list(binary_string), dtype=int)

def apply_delay(signal, angle_rad, kgrid_dt, is_positive, num_elements = 192, element_width = 0.2/1000, c0 = 1540):
    """
    Applique un retard temporel au signal pour chaque élément du transducteur.

    Args:
        signal (ndarray): Le signal acoustique initial.
        num_elements (int): Nombre total d'éléments.
        element_width (float): Largeur de chaque élément du transducteur.
        c0 (float): Vitesse du son dans le milieu (m/s).
        angle_rad (float): Angle d'inclinaison en radians.
        kgrid_dt (float): Pas de temps du kgrid.
        is_positive (bool): Indique si l'angle est positif ou négatif.

    Returns:
        ndarray: Tableau des signaux retardés.
    """
    delays = np.zeros(num_elements)
    for i in range(num_elements):
        delays[i] = (i * element_width * np.tan(angle_rad)) / c0  # Retard en secondes


    delay_samples = np.round(delays / kgrid_dt).astype(int)
    max_delay = np.max(np.abs(delay_samples))
    plt.figure(figsize=(12, 6))

    # Premier sous-graphique
    plt.figure()
    plt.plot(delays)
    plt.ylim([0, 10e-6])
    plt.title('Delays')
    plt.xlabel('Element')
    plt.ylabel('Delay (s)')

    # Afficher les graphiques
    plt.tight_layout()
    plt.show()
    delayed_signals = np.zeros((num_elements, len(signal) + max_delay))

    for i in range(num_elements):
        shift = delay_samples[i]
        if is_positive:
            delayed_signals[i, shift:shift + len(signal)] = signal  # Décalage à droite
        else:
            delayed_signals[i, max_delay - shift:max_delay - shift + len(signal)] = signal  # Décalage à gauche

    return delayed_signals
    
def getActiveListBin(path):
    base_name = os.path.basename(path)
    file = os.path.splitext(base_name)[0]
    start = file.index('_') + 1
    end = file.index('_', start)
    hexa = file[start:end]
    return hex_to_binary_array(hexa)

def getActiveListHexa(path):
    base_name = os.path.basename(path)
    file = os.path.splitext(base_name)[0]
    start = file.index('_') + 1
    end = file.index('_', start)
    return file[start:end]

def getAngle(path):
    base_name = os.path.basename(path)
    file = os.path.splitext(base_name)[0]
    angle_str = file[-3:]
    if angle_str[0] == '0':
        sign = 1
    else:
        sign = -1
    return sign * int(angle_str[1:])

def load_fieldHYDRO_XZ(file_path_h5, param_path_mat):    

    # Charger les fichiers .mat
    param = scipy.io.loadmat(param_path_mat)

    # Charger les paramètres
    x_test = param['x'].flatten()
    z_test = param['z'].flatten()

    x_range = np.arange(-23,21.2,0.2)
    z_range = np.arange(0,37.2,0.2)
    X, Z = np.meshgrid(x_range, z_range)

    # Charger le fichier .h5
    with h5py.File(file_path_h5, 'r') as file:
        data = file['data'][:]

    # Initialiser une matrice pour stocker les données acoustiques
    acoustic_field = np.zeros((len(z_range), len(x_range), data.shape[1]))

    # Remplir la grille avec les données acoustiques
    index = 0
    for i in range(len(z_range)):
        if i % 2 == 0:
            # Parcours de gauche à droite
            for j in range(len(x_range)):
                acoustic_field[i, j, :] = data[index]
                index += 1
        else:
            # Parcours de droite à gauche
            for j in range(len(x_range) - 1, -1, -1):
                acoustic_field[i, j, :] = data[index]
                index += 1

     # Calculer l'enveloppe analytique
    envelope = np.abs(hilbert(acoustic_field, axis=2))
    # Réorganiser le tableau pour avoir la forme (Times, Z, X)
    envelope_transposed = np.transpose(envelope, (2, 0, 1))
    return envelope_transposed

def load_fieldHYDRO_YZ(file_path_h5, param_path_mat):
    # Load parameters from the .mat file
    param = scipy.io.loadmat(param_path_mat)

    # Extract the ranges for y and z
    y_range = param['y'].flatten()
    z_range = param['z'].flatten()

    # Load the data from the .h5 file
    with h5py.File(file_path_h5, 'r') as file:
        data = file['data'][:]

    # Calculate the number of scans
    Ny = len(y_range)
    Nz = len(z_range)
    Nscans = Ny * Nz

    # Create the scan positions
    positions_y = []
    positions_z = []

    for i in range(Nz):
        if i % 2 == 0:
            # Traverse top to bottom for even rows
            positions_y.extend(y_range)
        else:
            # Traverse bottom to top for odd rows
            positions_y.extend(y_range[::-1])
        positions_z.extend([z_range[i]] * Ny)

    Positions = np.column_stack((positions_y, positions_z))

    # Initialize a matrix to store the reorganized data
    reorganized_data = np.zeros((Ny, Nz, data.shape[1]))

    # Reorganize the data according to the scan positions
    for index, (j, k) in enumerate(Positions):
        y_idx = np.where(y_range == j)[0][0]
        z_idx = np.where(z_range == k)[0][0]
        reorganized_data[y_idx, z_idx, :] = data[index, :]

    # Calculer l'enveloppe analytique
    envelope = np.abs(hilbert(reorganized_data, axis=2))
    # Réorganiser le tableau pour avoir la forme (Times, Z, Y)
    envelope_transposed = np.transpose(envelope, (2, 0, 1))
    return envelope_transposed, y_range, z_range

def load_fieldHYDRO_XYZ(file_path_h5, param_path_mat):
    # Load parameters from the .mat file
    param = scipy.io.loadmat(param_path_mat)

    # Extract the ranges for x, y, and z
    x_range = param['x'].flatten()
    y_range = param['y'].flatten()
    z_range = param['z'].flatten()

    # Create a meshgrid for x, y, and z
    X, Y, Z = np.meshgrid(x_range, y_range, z_range, indexing='ij')

    # Load the data from the .h5 file
    with h5py.File(file_path_h5, 'r') as file:
        data = file['data'][:]

    # Calculate the number of scans
    Nx = len(x_range)
    Ny = len(y_range)
    Nz = len(z_range)
    Nscans = Nx * Ny * Nz

    # Create the scan positions
    if Ny % 2 == 0:
        X = np.tile(np.concatenate([x_range[:, np.newaxis], x_range[::-1, np.newaxis]]), (Ny // 2, 1))
        Y = np.repeat(y_range, Nx)
    else:
        X = np.concatenate([x_range[:, np.newaxis], np.tile(np.concatenate([x_range[::-1, np.newaxis], x_range[:, np.newaxis]]), ((Ny - 1) // 2, 1))])
        Y = np.repeat(y_range, Nx)

    XY = np.column_stack((X.flatten(), Y))

    if Nz % 2 == 0:
        XYZ = np.tile(np.concatenate([XY, np.flipud(XY)]), (Nz // 2, 1))
        Z = np.repeat(z_range, Nx * Ny)
    else:
        XYZ = np.concatenate([XY, np.tile(np.concatenate([np.flipud(XY), XY]), ((Nz - 1) // 2, 1))])
        Z = np.repeat(z_range, Nx * Ny)

    Positions = np.column_stack((XYZ, Z))

    # Initialize a matrix to store the reorganized data
    reorganized_data = np.zeros((Nx, Ny, Nz, data.shape[1]))

    # Reorganize the data according to the scan positions
    for index, (i, j, k) in enumerate(Positions):
        x_idx = np.where(x_range == i)[0][0]
        y_idx = np.where(y_range == j)[0][0]
        z_idx = np.where(z_range == k)[0][0]
        reorganized_data[x_idx, y_idx, z_idx, :] = data[index, :]
    
    EnveloppeField = np.zeros_like(reorganized_data)

    for y in range(reorganized_data.shape[1]):
        for z in range(reorganized_data.shape[2]):
            EnveloppeField[:, y, z, :] = np.abs(hilbert(reorganized_data[:, y, z, :], axis=1))

    return EnveloppeField.T, x_range, y_range, z_range

def generate_2Dacoustic_field_KWAVE(angle_deg, active_listString, depth_end=37/1000, c0=1540, num_elements = 192, num_cycles = 4, element_width = 0.2/1000, depth_start = 0, f_US = 6e6, f_aq = 180e6, f_saving = 10e6, plotExcitation=True):
    
    active_listbin = ''.join(f"{int(active_listString[i:i+2], 16):08b}" for i in range(0, len(active_listString), 2))
    active_list = np.array([int(char) for char in active_listbin])

    # Grille
    probeWidth = num_elements * element_width
    Xrange = [-20 / 1000, 20 / 1000]  # Plage en X en mètres
    Zrange = [depth_start, depth_end ]  # Z range in meters for 289 time samples and 10° max

    t0 = floor(Zrange[0]/f_aq)
    tmax = ceil((depth_end -depth_start + probeWidth*np.tan(np.radians(abs(angle_deg))))*f_aq/c0)
 
    Nx = ceil((Xrange[1] - Xrange[0]) / element_width)
    Nz = ceil((Zrange[1] - Zrange[0]) / element_width)
    Nt = round(1.20 * (tmax - t0))

    dx = element_width
    dz = element_width

    # Print the results
    print("Xrange:", Xrange)
    print("Zrange:", Zrange)
    print("Nx:", Nx)
    print("Nz:", Nz)
    print("dx:",dx)
    print("dz:",dz)
    print("Angles : ",angle_deg)
    print("Active List : ",active_listString)

    kgrid = kWaveGrid([Nx, Nz], [dx, dz])
    kgrid.setTime(Nt = Nt, dt = 1/f_aq)

    # Définir le medium
    # medium = kWaveMedium(sound_speed=1540, density=1000, alpha_coeff=0.75, alpha_power=1.5, BonA=6)
    medium = kWaveMedium(sound_speed=c0)
    
    # Génération du signal de base
    signal = tone_burst(f_aq, f_US, num_cycles).squeeze() # * 1.5 pour faire comme dans Field2

    if plotExcitation:
        time2plot = np.arange(0, len(signal)) / f_aq
        plt.figure(figsize=(8, 8))
        plt.plot(time2plot,signal)
        plt.title('Excitation Signal')
        plt.xlabel('Time (samples)')
        plt.ylabel('Amplitude')
        plt.grid()
        plt.show()

    # Masque de la sonde : alignée dans le plan XZ
    source = kSource()
    source.p_mask = np.zeros((Nx, Nz))  # Crée une grille vide pour le masque de la source
 
    # Placement des transducteurs actifs dans le masque
    for i in range(num_elements):
        if active_list[i] == 1:  # Vérifiez si l'élément est actif
            x_pos = i  # Position des éléments sur l'axe X
            source.p_mask[x_pos, 0] = 1  # Position dans le plan XZ

    source.p_mask = source.p_mask.astype(int)  # Conversion en entier
    # print("Number of active elements in p_mask:", np.sum(source.p_mask))
    is_positive_angle = angle_deg >= 0
    # Inclinaison de la sonde (en degrés)
    angle_rad = np.radians(abs(angle_deg))  # Convertir en radians

    delayed_signals = apply_delay(signal, angle_rad, kgrid.dt, is_positive_angle)
    # Filtrer les signaux pour correspondre aux éléments actifs
    delayed_signals_active = delayed_signals[active_list == 1, :]
    source.p = delayed_signals_active  # Transposer pour que chaque colonne corresponde à un élément actif

    # === Définir les capteurs pour observer les champs acoustiques ===
    sensor = kSensor()
    sensor.mask = np.ones((Nx, Nz))  # Capteur couvrant tout le domaine

    isGPU, bestGPU = select_best_gpu()

    # === Options de simulation ===
    simulation_options = SimulationOptions(
        pml_inside=False,  # Empêche le PML d'être ajouté à l'intérieur de la grille
        pml_x_size=20,      # Taille de la PML sur l'axe X
        pml_z_size=20,       # Taille de la PML sur l'axe Z    
        use_sg= False,
        save_to_disk = True,
        input_filename=os.path.join(gettempdir(),"KwaveIN.h5"),
        output_filename= os.path.join(gettempdir(),"KwaveOUT.h5"))

    execution_options = SimulationExecutionOptions(
        is_gpu_simulation=isGPU,
        device_num = bestGPU)
    
    # === Lancer la simulation ===
    print("Lancement de la simulation...")
    sensor_data = kspaceFirstOrder2D(
        kgrid=kgrid,
        medium=medium,
        source=source,
        sensor=sensor,
        simulation_options=simulation_options,
        execution_options=execution_options,
    )
    print("Simulation terminée avec succès.")

    return sensor_data['p'].reshape(kgrid.Nt,Nz, Nx)

def generate_3Dacoustic_field_KWAVE(angle_deg, active_listString, depth_end=37/1000, c0=1540, num_elements = 192, num_cycles = 4, element_width = 0.2/1000, element_height = 6/1000, depth_start = 0, f_US = 6e6, f_aq = 180e6, f_saving = 10e6, IsSaving=True):

    active_listbin = ''.join(f"{int(active_listString[i:i+2], 16):08b}" for i in range(0, len(active_listString), 2))
    active_list = np.array([int(char) for char in active_listbin])

    print(active_list.shape)
    
    # Grille
    probeWidth = num_elements * element_width
    Xrange = [-20 / 1000, 20 / 1000]  # Plage en X en mètres
    Yrange = [-element_height * 5 / 2, element_height * 5 / 2]  # Plage en Y en mètres
    Zrange = [depth_start, depth_end]  # Plage en Z en mètres

    dx = element_width
    dz = dx
    dy = dx

    t0 = floor(Zrange[0] / f_aq)
    tmax = ceil((depth_end -depth_start + probeWidth*np.tan(np.radians(abs(angle_deg))))*f_aq/c0)
    print(f"t_max : {tmax}")
    Nx = ceil((Xrange[1] - Xrange[0]) / element_width)
    Ny = 4 * ceil((Yrange[1] - Yrange[0]) / element_height)
    Nz = ceil((Zrange[1] - Zrange[0]) / element_width)
    Nt = round(1.2 * (tmax - t0))

    # Print the results
    print("Xrange:", Xrange)
    print("Yrange:", Yrange)
    print("Zrange:", Zrange)
    print("Nx:", Nx)
    print("Ny:", Ny)
    print("Nz:", Nz)
    print("dx:",dx)
    print("dy:",dy)
    print("dz:",dz)
    print("Angles : ",angle_deg)
    print("Active List : ",active_listString)
    print("Nt:", Nt)

    # Initialisation de la grille et du milieu
    kgrid = kWaveGrid([Nx, Ny, Nz], [element_width, element_height, dx])
    kgrid.setTime(Nt=Nt, dt=1/f_aq)
    medium = kWaveMedium(sound_speed=c0)

    # Génération du signal de base
    signal = tone_burst(f_aq, f_US, num_cycles).squeeze() # * 1.5 pour faire comme dans Field2

    # Masque de la sonde : alignée dans le plan XZ
    source = kSource()
    source.p_mask = np.zeros((Nx, Ny, Nz))  # Crée une grille vide pour le masque de la source

    stringList = ''.join(map(str, active_list))
    print(stringList)
 
    # Placement des transducteurs actifs dans le masque
    for i in range(num_elements):
        if active_list[i] == 1:  # Vérifiez si l'élément est actif
            x_pos = i+Nx//2 - num_elements//2 # Position des éléments sur l'axe X
            source.p_mask[x_pos, Ny // 2, 0] = 1  # Position dans le plan XZ

    source.p_mask = source.p_mask.astype(int)  # Conversion en entier
    # print("Number of active elements in p_mask:", np.sum(source.p_mask))
    is_positive_angle = angle_deg >= 0
    # Inclinaison de la sonde (en degrés)
    angle_rad = np.radians(abs(angle_deg))  # Convertir en radians

    delayed_signals = apply_delay(signal, angle_rad, kgrid.dt, is_positive_angle, num_elements, element_width, c0)

    # Filtrer les signaux pour correspondre aux éléments actifs
    delayed_signals_active = delayed_signals[active_list == 1, :]
    source.p = delayed_signals_active  # Transposer pour que chaque colonne corresponde à un élément actif

    # === Définir les capteurs pour observer les champs acoustiques ===
    sensor = kSensor()
    sensor.mask = np.ones((Nx, Ny, Nz))  # Capteur couvrant tout le domaine

    isGPU, bestGPU = select_best_gpu()

    # === Options de simulation ===
    simulation_options = SimulationOptions(
        pml_inside=False,  # Empêche le PML d'être ajouté à l'intérieur de la grille
        pml_auto = True, 
        use_sg= False, 
        save_to_disk = True,
        input_filename=os.path.join(gettempdir(),"KwaveIN.h5"),
        output_filename= os.path.join(gettempdir(),"KwaveOUT.h5"))
    
    execution_options = SimulationExecutionOptions(
        is_gpu_simulation=isGPU,
        device_num = bestGPU)

    # === Lancer la simulation ===
    print("Lancement de la simulation...")
    sensor_data = kspaceFirstOrder3D(
        kgrid=kgrid,
        medium=medium,
        source=source,
        sensor=sensor,
        simulation_options=simulation_options,
        execution_options=execution_options,
    )
    print("Simulation terminée avec succès.")
    return sensor_data['p'].reshape(kgrid.Nt,Nz, Ny, Nx)

def calculate_envelope_squared(acoustic_field):
    """
    Calculate the analytic envelope of the acoustic field.

    Parameters:
    - acoustic_field (numpy.ndarray or cupy.ndarray): Input acoustic field data. This should be a time-domain signal.

    Returns:
    - envelope (numpy.ndarray or cupy.ndarray): The squared analytic envelope of the acoustic field.
    """
    acoustic_field_gpu = cp.asarray(acoustic_field)

    if len(acoustic_field_gpu.shape) not in [3, 4]:
        raise ValueError("Input acoustic field must be a 3D or 4D array.")

    if len(acoustic_field_gpu.shape) == 3:
        envelope_gpu = cp.abs(cp_hilbert(acoustic_field_gpu, axis=0))**2
    elif len(acoustic_field_gpu.shape) == 4:
        EnveloppeField = cp.zeros_like(acoustic_field_gpu)
        for y in range(acoustic_field_gpu.shape[2]):
            for z in range(acoustic_field_gpu.shape[1]):
                EnveloppeField[:, z, y, :] = cp.abs(cp_hilbert(acoustic_field_gpu[:, z, y, :], axis=1))**2
        envelope_gpu = EnveloppeField

    # Convert the result back to a NumPy array
    return cp.asnumpy(envelope_gpu)
    
def save_fieldKWAVE_XZ(acoustic_field, filePath, f0=6e6, num_elements =192, dx = 0.2/1000):
    """
    Fonction Python qui reproduit la logique de la méthode SaveField du code MATLAB.

    Paramètres :
    - obj : Objet contenant les paramètres (comme obj.param en MATLAB).
    - acoustic_field : Données du champ acoustique (MySimulationBox.Field en MATLAB).
    - num_elements : Nombre total d'éléments de la sonde.
    - structuration : Structure d'activation des transducteurs.
    - folderPath : Chemin où les fichiers .img et .hdr seront enregistrés.
    """
    t_ex = 1/f0

    active_list_hex = getActiveListHexa(filePath)
    active_list_bin = ''.join(map(str,getActiveListBin(filePath)))

    angle = getAngle(filePath)
    angle_sign = '1' if angle < 0 else '0'
    formatted_angle = f"{angle_sign}{abs(angle):02d}"

    # 4. Définir les noms de fichiers (img et hdr)
    file_name = f"field_{active_list_hex}_{formatted_angle}"

    img_path = os.path.join(Path(filePath).parent , file_name + ".img")
    hdr_path = os.path.join(Path(filePath).parent , file_name + ".hdr")
    

    # === 3. Sauvegarder le champ acoustique dans le fichier .img ===
    with open(img_path, "wb") as f_img:
        acoustic_field.astype('float32').tofile(f_img)  # Sauvegarde au format float32 (équivalent à "single" en MATLAB)
    
    # === 4. Création du contenu du fichier .hdr ===
    x_range = [0, acoustic_field.shape[2] * dx]
    z_range = [0, acoustic_field.shape[1] * dx]
    x_pixel_size = dx  # En mm/pixel
    z_pixel_size = dx  # En mm/pixel
    time_pixel_size = 1 / 25e6  # En s/pixel
    first_pixel_offset_x = x_range[0] * 1e3  # En mm
    first_pixel_offset_z = z_range[0] * 1e3  # En mm
    first_pixel_offset_t = 0

    # **Génération du headerFieldGlob**
    headerFieldGlob = (
        f"!INTERFILE :=\n"
        f"modality : AOT\n"
        f"voxels number transaxial: {acoustic_field.shape[2]}\n"
        f"voxels number transaxial 2: {acoustic_field.shape[1]}\n"
        f"voxels number axial: {1}\n"
        f"field of view transaxial: {(x_range[1] - x_range[0]) * 1000}\n"
        f"field of view transaxial 2: {(z_range[1] - z_range[0]) * 1000}\n"
        f"field of view axial: {1}\n"
    )

    # **Génération du header**
    header = (
        f"!INTERFILE :=\n"
        f"!imaging modality := AOT\n\n"
        f"!GENERAL DATA :=\n"
        f"!data offset in bytes := 0\n"
        f"!name of data file := system_matrix/{file_name}.img\n\n"
        f"!GENERAL IMAGE DATA\n"
        f"!total number of images := {acoustic_field.shape[0]}\n"
        f"imagedata byte order := LITTLEENDIAN\n"
        f"!number of frame groups := 1\n\n"
        f"!STATIC STUDY (General) :=\n"
        f"number of dimensions := 3\n"
        f"!matrix size [1] := {acoustic_field.shape[2]}\n"
        f"!matrix size [2] := {acoustic_field.shape[1]}\n"
        f"!matrix size [3] := {acoustic_field.shape[0]}\n"
        f"!number format := short float\n"
        f"!number of bytes per pixel := 4\n"
        f"scaling factor (mm/pixel) [1] := {x_pixel_size * 1000}\n"
        f"scaling factor (mm/pixel) [2] := {z_pixel_size * 1000}\n"
        f"scaling factor (s/pixel) [3] := {time_pixel_size}\n"
        f"first pixel offset (mm) [1] := {first_pixel_offset_x}\n"
        f"first pixel offset (mm) [2] := {first_pixel_offset_z}\n"
        f"first pixel offset (s) [3] := {first_pixel_offset_t}\n"
        f"data rescale offset := 0\n"
        f"data rescale slope := 1\n"
        f"quantification units := 1\n\n"
        f"!SPECIFIC PARAMETERS :=\n"
        f"angle (degree) := {angle}\n"
        f"activation list := {active_list_bin}\n"
        f"number of US transducers := {num_elements}\n"
        f"delay (s) := 0\n"
        f"us frequency (Hz) := {f0}\n"
        f"excitation duration (s) := {t_ex}\n"
        f"!END OF INTERFILE :=\n"
    )

    # === 5. Sauvegarder le fichier .hdr ===
    with open(hdr_path, "w") as f_hdr:
        f_hdr.write(header)

    with open(os.path.join(Path(filePath).parent ,"field.hdr"), "w") as f_hdr2:
        f_hdr2.write(headerFieldGlob)

def load_fieldKWAVE_XZ(hdr_path):
    """
    Lit un fichier Interfile (.hdr) et son fichier binaire (.img) pour reconstruire un champ acoustique.

    Paramètres :
    ------------
    - folderPathBase : dossier de base contenant les fichiers
    - hdr_path : chemin relatif du fichier .hdr depuis folderPathBase

    Retour :
    --------
    - field : tableau NumPy contenant le champ acoustique avec les dimensions réordonnées en (X, Z, time)
    - header : dictionnaire contenant les métadonnées du fichier .hdr
    """
    header = {}
    # Lecture du fichier .hdr
    with open(hdr_path, 'r') as f:
        for line in f:
            if ':=' in line:
                key, value = line.split(':=', 1)
                key = key.strip().lower().replace('!', '')
                value = value.strip()
                header[key] = value


    # Récupère le nom du fichier .img associé
    data_file = header.get('name of data file') or header.get('name of date file')
    if data_file is None:
        raise ValueError(f"Impossible de trouver le fichier de données associé au fichier header {hdr_path}")
    img_path = os.path.join(os.path.dirname(hdr_path),os.path.basename(data_file))

    # Détermine la taille du champ à partir des métadonnées
    shape = [int(header[f'matrix size [{i}]']) for i in range(1, 3) if f'matrix size [{i}]' in header]
    if not shape:
        raise ValueError("Impossible de déterminer la forme du champ acoustique à partir des métadonnées.")

    # Type de données
    data_type = header.get('number format', 'short float').lower()
    dtype_map = {
        'short float': np.float32,
        'float': np.float32,
        'int16': np.int16,
        'int32': np.int32,
        'uint16': np.uint16,
        'uint8': np.uint8
    }
    dtype = dtype_map.get(data_type)
    if dtype is None:
        raise ValueError(f"Type de données non pris en charge : {data_type}")

    # Ordre des octets (endianness)
    byte_order = header.get('imagedata byte order', 'LITTLEENDIAN').lower()
    endianess = '<' if 'little' in byte_order else '>'

    # Vérifie la taille réelle du fichier .img
    fileSize = os.path.getsize(img_path)
    timeDim = int(fileSize / (np.dtype(dtype).itemsize *np.prod(shape)))
        # if img_size != expected_size:
    #     raise ValueError(f"La taille du fichier img ({img_size} octets) ne correspond pas à la taille attendue ({expected_size} octets).")
    shape = shape + [timeDim]
    # Lecture des données binaires
    with open(img_path, 'rb') as f:
        data = np.fromfile(f, dtype=endianess + np.dtype(dtype).char)

    # Reshape les données en (time, Z, X)
    field = data.reshape(shape[::-1])  # NumPy interprète dans l'ordre C (inverse de MATLAB)



    # Applique les facteurs d'échelle si disponibles
    rescale_slope = float(header.get('data rescale slope', 1))
    rescale_offset = float(header.get('data rescale offset', 0))
    field = field * rescale_slope + rescale_offset

    return field
