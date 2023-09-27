# PopYou!

PopYou! is a project to create custom Funko Pop figures from text and images. With PopYou!, you can bring your favorite characters and ideas to life in the iconic Funko Pop style.
Using Gans and not diffusion, such that the runtime and memory requirements are much lower.


## Method

first I generated 30000 images of funko using [deci diffusion](https://deci.ai/blog/decidiffusion-1-0-3x-faster-than-stable-diffusion-same-quality/).
Then I used the dataset to train a GAN model using FastGan and the results are below.

![FastGan examples](assets/fast_gan_examples.jpg)

after that I froze the gan and created an inversion model using frozen clip as backbone,
this gives the inversion model the ability to generate images from text and from images in other domains such as real images of people and faces.


the examples below are generated using the inversion model such that the
text given is "funko pop figure of {name} in a white background".


| Celebrty Name    | PopYou! Model | [deci diffusion](https://deci.ai/blog/decidiffusion-1-0-3x-faster-than-stable-diffusion-same-quality/) |
|------------------|---------------|--------------------------------------------------------------------------------------------------------|
| Barack Obama     | <img src="assets/Barack_Obama_fastgan.png" width="200"> | <img src="assets/Barack_Obama_deci.png" width="200">                                                   |
| Alan Turing      | <img src="assets/Alan_Turing_fastgan.png" width="200"> | <img src="assets/Alan_Turing_deci.png" width="200">                                                    |
| Elsa from frozen | <img src="assets/Elsa_fastgan.png" width="200"> | <img src="assets/Elsa_deci.png" width="200">                                                           |


these are examples using the clip image encoding of a face of the person.

| Celebrty Name        | Image                                                        | PopYou! Model                                                 |
|----------------------|--------------------------------------------------------------|---------------------------------------------------------------|
| Sun from Lost        | <img src="assets/sun_Lost_image.webp" width="200">           | <img src="assets/sun_Lost_fastgan.png" width="200">           |
| Bon from Lost        | <img src="assets/bon_Lost_image.webp" width="200">           | <img src="assets/bon_Lost_fastgan.png" width="200">           |
| Ras from SiliconValley | <img src="assets/ras_SiliconValley_image.webp" width="200">  | <img src="assets/ras_SiliconValley_fastgan.png" width="200">  |
| Lori from SiliconValley | <img src="assets/lori_SiliconValley_image.jpeg" width="200"> | <img src="assets/lori_SiliconValley_fastgan.png" width="200"> |


these are examples using the clip text encoding when it uses the prfiex " funko pop figure of a {text} in a white background".

| text                    | PopYou! Model                                     | clip similarty |
|-------------------------|---------------------------------------------------|----------------|
| tall man with a beard and a black shirt          | <img src="assets/text_1_example.png" width="200"> | 0.389          |
| woman with a blonde short hair           | <img src="assets/text_2_example.png" width="200"> | 0.342          |
| cool man in suite and glasses  | <img src="assets/text_3_example.png" width="200"> | 0.354          |
| tall thin man with blue pants and black hair  | <img src="assets/text_4_example.png" width="200"> | 0.380          |


## 3D Generation

Using the latest advancement in diffusion models and textual inversion, we can generate the pop as a mesh or generate it from diffrent views.
Also we can use textual inversion to generate the pop with stable diffusion, for more information read about textual inversion.
example of images generated using ["SyncDreamer: Generating Multiview-consistent Images from a Single-view Image"(2023)](https://arxiv.org/abs/2309.03453)


| PopYou! Image generated | SyncDreamer 3d renders output                    |
|-------------------------|--------------------------------------------------|
| <img src="assets/Alan_Turing_fastgan.png" width="200">                    | <img src="assets/alan_turing_3d.png"> |
| <img src="assets/ras_SiliconValley_fastgan.png" width="200">                     | <img src="assets/ras_3d.png">         |

## Results

|                 | PopYou! | deci diffusion |
|-----------------|---------|----------------|
| clip similarity | 0.31    | 0.33           |
| Fid             | 562     | 258            |

Note:
The fid is calculate between a folder generated from the model and the real images of funko pop.
The clip similarity is calculated between the text and the image generated from the model, it uses the text prefix above and a list 300 famous people.