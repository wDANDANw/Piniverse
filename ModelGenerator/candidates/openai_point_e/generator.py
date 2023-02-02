# Common
import torch
from tqdm.auto import tqdm
import os

# Common Point E
from candidates.openai_point_e.point_e.models.download import load_checkpoint
from candidates.openai_point_e.point_e.models.configs import MODEL_CONFIGS, model_from_config
from candidates.openai_point_e.point_e.util.plotting import plot_point_cloud

# Point Cloud Generation
from candidates.openai_point_e.point_e.diffusion.configs import DIFFUSION_CONFIGS, diffusion_from_config
from candidates.openai_point_e.point_e.diffusion.sampler import PointCloudSampler

# Mesh Generation
from PIL import Image
import matplotlib.pyplot as plt
from candidates.openai_point_e.point_e.util.pc_to_mesh import marching_cubes_mesh
from candidates.openai_point_e.point_e.util.point_cloud import PointCloud

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

SHOW_FIG = False

def text_to_mesh(query):
    pc = text_to_pc(query)
    mesh = pc_to_mesh(pc)

    return mesh

def text_to_pc(query):
    print('creating base model...')
    base_name = 'base40M-textvec'
    base_model = model_from_config(MODEL_CONFIGS[base_name], device)
    base_model.eval()
    base_diffusion = diffusion_from_config(DIFFUSION_CONFIGS[base_name])

    print('creating upsample model...')
    upsampler_model = model_from_config(MODEL_CONFIGS['upsample'], device)
    upsampler_model.eval()
    upsampler_diffusion = diffusion_from_config(DIFFUSION_CONFIGS['upsample'])

    print('downloading base checkpoint...')
    base_model.load_state_dict(load_checkpoint(base_name, device))

    print('downloading upsampler checkpoint...')
    upsampler_model.load_state_dict(load_checkpoint('upsample', device))

    sampler = PointCloudSampler(
        device=device,
        models=[base_model, upsampler_model],
        diffusions=[base_diffusion, upsampler_diffusion],
        num_points=[1024, 4096 - 1024],
        aux_channels=['R', 'G', 'B'],
        guidance_scale=[3.0, 0.0],
        model_kwargs_key_filter=('texts', ''),  # Do not condition the upsampler at all
    )

    # Set a prompt to condition on.
    # prompt = 'Red Corgi in yellow shirt'

    # Produce a sample from the model.
    samples = None
    for x in tqdm(sampler.sample_batch_progressive(batch_size=1, model_kwargs=dict(texts=[query]))):
        samples = x

    pc = sampler.output_to_point_clouds(samples)[0]

    if (SHOW_FIG):
        fig = plot_point_cloud(pc, grid_size=3, fixed_bounds=((-0.75, -0.75, -0.75), (0.75, 0.75, 0.75)))
        fig.show()

    return pc

def pc_to_mesh(pc):
    print('creating SDF model...')
    name = 'sdf'
    model = model_from_config(MODEL_CONFIGS[name], device)
    model.eval()

    print('loading SDF model...')
    model.load_state_dict(load_checkpoint(name, device))
    #%%
    # Load a point cloud we want to convert into a mesh.
    # pc = PointCloud.load('example_data/pc_corgi.npz')

    # Plot the point cloud as a sanity check.
    # fig = plot_point_cloud(pc, grid_size=2)
    #%%
    # Produce a mesh (with vertex colors)
    mesh = marching_cubes_mesh(
        pc=pc,
        model=model,
        batch_size=4096,
        grid_size=32, # increase to 128 for resolution used in evals
        progress=True,
    )



    #%%
    # Write the mesh to a PLY file to import into some other program.
    with open('../mesh.ply', 'wb') as f:
        mesh.write_ply(f)

    # Send back file path
    return os.path.abspath("../mesh.ply")


