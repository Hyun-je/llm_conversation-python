# import common module
import argparse
import asyncio

# import my module
import network
import voice



async def main(args):

    # Setup voice synthesizer
    print('load voice synth')
    synthesizer = voice.VoiceSynthesizer()

    # Setup llm client
    answer = ""

    # Setup network manager
    network_manager = network.UDPManager()
    
    def on_receive_text_generation(data, addr):
        print(f"on_receive_text_generation: {data} {addr=}")
        answer = input('>>> ')
        dict = {
            'message': answer
        }
        network_manager.sender.send_dict('text_generation', dict)
    network_manager.add_callback('text_generation', on_receive_text_generation)

    def on_receive_speech_completion(data, addr):
        print(f"on_receive_speech_completion: {data} {addr=}")
        print('synthesis voice...')
        synthesizer.synthesis(answer)
    network_manager.add_callback('speech_completion', on_receive_speech_completion)
    
    print('Ready!')
    on_receive_text_generation(None, None)
    await network_manager.run()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--target', required=False, help='어느 것을 요구하냐')
    parser.add_argument('--env', required=False, default='dev', help='실행환경은 뭐냐')
    args = parser.parse_args()

    asyncio.run(main(args))