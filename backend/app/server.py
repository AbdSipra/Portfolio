#THIS FILE WILL RUN THE gRPC SERVER

<<<<<<< HEAD
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import grpc
from concurrent import futures
from protos import audio_pb2_grpc
from protos import audio_pb2



# jb bark model ready hojai ga tou idher to wo import krna hai
from model import bark_model

class StoryAudioService(audio_pb2_grpc.StoryAudioServiceServicer):
    def __init__(self):
        #bark model initialisation
        #self.model = Story2AudioModel()
        pass 

    def GenerateAudio(self, request, context):
        story_text = request.story_text
        print(f"Recieved story text {story_text}")

        #for now jb tk model nae hai return this fake audio for testing 
        fake_audio = b"This is a fake audio for testing purposes"

        #audio_bytes = self.model.generate_audio(story_text)

        return audio_pb2.AudioResponse(audio_data=fake_audio)
    
#Serve the generated audio 
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    audio_pb2_grpc.add_StoryAudioServiceServicer_to_server(StoryAudioService(), server)
    server.add_insecure_port('[::]:50051')  # Listen on all available IPs, port 50051
    server.start()
    print("✅ gRPC server started. Listening on port 50051...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
        


>>>>>>> 541976ddbcaa355a46739796716fec08fed05f09
