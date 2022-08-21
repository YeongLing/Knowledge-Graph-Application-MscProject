import pickle
from collections import defaultdict

dict={'function':'function','sideeffects':'supplier','protein':'system','drug':'designer','disease':'component','psoriatic_arthritis':'bearings','sleep_disorder':'bearing_clamps','sexual_disorder':'terminal_Box','developmental_disorder_of_mental_health':'terminal_box_lid','parasitic_infectious_disease':'end_bells','viral_infectious_disease':'housing','polycystic_ovary_syndrome':'floor_pan','reproductive_system_disease':'motor_mounts','fungal_infectious_disease':'three_phase_lines','bacterial_infectious_disease':'LV_harness','urinary_system_disease':'motor_shaft','respiratory_system_disease':'resolver_stator','benign_neoplasm':'resolver_rotor','hypospadias':'resolver_clamp','pre-malignant_neoplasm':'resolver_adapter','cancer':'rotor_core','cardiovascular_system_disease':'rotor_laminations','orofacial_cleft':'stator_lamination','somatoform_disorder':'stator_windings','irritable_bowel_syndrome':'DC_AC_converter','inherited_metabolic_disorder':'bumper','gastrointestinal_system_disease':'timing_belt','immune_system_disease':'pressure_sensor','musculoskeletal_system_disease':'main_chasis','acquired_metabolic_disease':'realsense_camera','substance-related_disorder':'motor_driver','cryptorchidism':'power_connector','personality_disorder':'haldle','integumentary_system_disease':'working_screw','thoracic_disease':'adapter','endocrine_system_disease':'outer_casing','monogenic_disease':'dust_filter','cognitive_disorder':'RGBD_camera','hematopoietic_system_diseases':'track_rim','chromosomal_disease':'gear_box','hematopoietic_system_disease':'end_effector','nervous_system_disease':'motion_power_unit','struct_sim':'control_unit','ptmod':'joint','catalysis':'power','activation':'motion_control','inhibition':'control','reaction':'human_robot_interaction','expression':'data_acquisition','binding':'feedback'}
obj=pickle.load(open('..\\bio_data\\graph_data.pkl','rb'))
obj_0,obj_1,obj_2=defaultdict(list),{},defaultdict(list)

for k,v in obj[0].items():
    key,value=dict[k],[]
    for t in v:
        t1,t2=t[0],t[1]
        value.append((dict[t1],dict[t[1]] if t[1]!='0' else t[1]))
    obj_0[key]=value

for k,v in obj[1].items():
    n1,rel,n2=k[0],k[1],k[2]
    key=(dict[n1],dict[rel] if rel!='0' else rel,dict[n2])
    obj_1[key]=v

for k,v in obj[2].items():
    key=dict[k]
    obj_2[key]=v

res=(obj_0,obj_1,obj_2)
f=open('..\\engineering_data\\graph_data.pkl','wb')
pickle.dump(res,f)
f.close()


