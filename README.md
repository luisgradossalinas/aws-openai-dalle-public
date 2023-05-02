# AWS integration with Dall-e (OpenAI) and WhatsApp

<img width="900" src="https://user-images.githubusercontent.com/2066453/235762189-ece5ec56-84aa-4fc3-97fe-0e265a69d36f.png">

## Requisitos

- [Tener una cuenta en AWS](https://gist.github.com/luisgradossalinas/c233c0333022c6617dd70609bfdf6441)
- [Tener una cuenta en OpenAI](https://gist.github.com/luisgradossalinas/45c1c5ed27b7f73e0d3cf3bc0fbe846d)
- [Tener una cuenta en UltraMSG](https://gist.github.com/luisgradossalinas/1380c0b42f85ed3a46e7e9ede4249f09)

## Accedemos a nuestra cuenta de AWS y creamos un entorno de Cloud9, donde clonaremos el repositorio.

Ejecutar en Cloud9.

	git clone https://github.com/luisgradossalinas/aws-openai-dalle-public

Abrir el contenido del archivo falle.yaml e ingresamos en la línea 66 nuestro API Key de OpenAI.

![image](https://user-images.githubusercontent.com/2066453/235266795-fc85d4a8-ef15-49ea-93b9-b4a93cabf922.png)

En la línea 73, ingresar el valor de nuestra instancia y token de UltraMsg.

Ejecutar en Cloud9

	cd aws-openai-dalle
	sh sh/01_Start_Deploy.sh

Esperamos que se cree el stack en CloudFormation.

Ejecutar el python generate-image.py en Cloud9 (Enviará un mensaje a Kinesis Data Streams que será leído por una función Lambda)

	python3 generate-image.py

Esperamos unos segundos y recibiremos un mensaje por WhatsApp con la imagen generado por Dall-e.

<img width="891" src="https://user-images.githubusercontent.com/2066453/235746888-fd399803-6466-43ed-aa4a-a94a7439e5f3.png">

<img width="891" src="https://user-images.githubusercontent.com/2066453/235746557-d2619798-95cc-4041-addd-a6a37b9fc004.png">

<img width="491" src="https://user-images.githubusercontent.com/2066453/235746691-7b926dd2-56d9-4451-a53f-17591494b3aa.png">

## Documentación

https://realpython.com/generate-images-with-dalle-openai-api

https://github.com/openai/openai-cookbook/blob/main/examples/dalle/Image_generations_edits_and_variations_with_DALL-E.ipynb

## Agradecimientos

Espero te haya servido esta solución, si pudiste replicarlo, puedes publicarlo en LinkedIn con tus aportes, cambios y etiquétame (https://www.linkedin.com/in/luisgrados).

## Eliminar recursos en AWS

Ejecutamos en Cloud9.

    aws s3 ls | grep dalle-images | awk {'print "aws s3 rb s3://" $3 " --f"'} | sh
    aws s3 ls | grep dalle-code | awk {'print "aws s3 rb s3://" $3 " --f"'} | sh   
    aws cloudformation delete-stack --stack-name StackDalle
    echo "Stack StackDalle eliminándose"
