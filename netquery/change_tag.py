import pickle
import joblib
from collections import  defaultdict

#替换字典
dict={'function':'function','sideeffects':'supplier','protein':'system','drug':'designer','disease':'component','psoriatic_arthritis':'bearings','sleep_disorder':'bearing_clamps','sexual_disorder':'terminal_Box','developmental_disorder_of_mental_health':'terminal_box_lid','parasitic_infectious_disease':'end_bells','viral_infectious_disease':'housing','polycystic_ovary_syndrome':'floor_pan','reproductive_system_disease':'motor_mounts','fungal_infectious_disease':'three_phase_lines','bacterial_infectious_disease':'LV_harness','urinary_system_disease':'motor_shaft','respiratory_system_disease':'resolver_stator','benign_neoplasm':'resolver_rotor','hypospadias':'resolver_clamp','pre-malignant_neoplasm':'resolver_adapter','cancer':'rotor_core','cardiovascular_system_disease':'rotor_laminations','orofacial_cleft':'stator_lamination','somatoform_disorder':'stator_windings','irritable_bowel_syndrome':'DC_AC_converter','inherited_metabolic_disorder':'bumper','gastrointestinal_system_disease':'timing_belt','immune_system_disease':'pressure_sensor','musculoskeletal_system_disease':'main_chasis','acquired_metabolic_disease':'realsense_camera','substance-related_disorder':'motor_driver','cryptorchidism':'power_connector','personality_disorder':'haldle','integumentary_system_disease':'working_screw','thoracic_disease':'adapter','endocrine_system_disease':'outer_casing','monogenic_disease':'dust_filter','cognitive_disorder':'RGBD_camera','hematopoietic_system_diseases':'track_rim','chromosomal_disease':'gear_box','hematopoietic_system_disease':'end_effector','nervous_system_disease':'motion_power_unit','struct_sim':'control_unit','ptmod':'joint','catalysis':'power','activation':'motion_control','inhibition':'control','reaction':'human_robot_interaction','expression':'data_acquisition','binding':'feedback'}
#输入要查看的文件名称
#obj=pickle.load(open('..\\engineering_data\\train_edges.pkl','rb'))
obj=joblib.load(open('..\\bio_data\\test_edges.pkl','rb'))
res=[]
for t in obj:
    t=((t[0][0],(t[0][1][0],(dict[t[0][1][1][0]],dict[t[0][1][1][1]] if t[0][1][1][1]!='0' else t[0][1][1][1],dict[t[0][1][1][2]]),t[0][1][2])),t[1],t[2])
    res.append(t)

f=open('..\\engineering_data\\test_edges.pkl','wb')
pickle.dump(res,f)
f.close()