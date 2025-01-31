/// @file

#include <iostream>
#include <fstream>
#include <string.h>
#include <errno.h>

#include "wavfile_mono.h"
#include "pitch_analyzer.h"

#include "docopt.h"

#define FRAME_LEN   0.030 /* 30 ms. */
#define FRAME_SHIFT 0.015 /* 15 ms. */

using namespace std;
using namespace upc;

static const char USAGE[] = R"(
get_pitch - Pitch Estimator 

Usage:
    get_pitch [options] <input-wav> <output-txt>
    get_pitch (-h | --help)
    get_pitch --version

Options:
    -m REAL, --umaxnorm=REAL    Umbral del maximo de la autocorrelacion [default: 0.6]
    -n REAL, --u1norm=REAL      Umbral 1norm [default: 1]
    -p REAL, --upot=REAL        Umbral potencia [default: 6]
    -h, --help  Show this screen
    --version   Show the version of the project

Arguments:
    input-wav   Wave file with the audio signal
    output-txt  Output file: ASCII file with the result of the estimation:
                    - One line per frame with the estimated f0
                    - If considered unvoiced, f0 must be set to f0 = 0
)";

int main(int argc, const char *argv[]) {
	/// \TODO 
	///  Modify the program syntax and the call to **docopt()** in order to
	///  add options and arguments to the program.
    std::map<std::string, docopt::value> args = docopt::docopt(USAGE,
        {argv + 1, argv + argc},	// array of arguments, without the program name
        true,    // show help if requested
        "2.0");  // version string

	std::string input_wav = args["<input-wav>"].asString();
	std::string output_txt = args["<output-txt>"].asString();
  float umaxnorm = stof(args["--umaxnorm"].asString());
  float upot=stof(args["--upot"].asString());
  float u1norm =stof(args["--u1norm"].asString());
  // Read input sound file
  unsigned int rate;
  vector<float> x;
  if (readwav_mono(input_wav, rate, x) != 0) {
    cerr << "Error reading input file " << input_wav << " (" << strerror(errno) << ")\n";
    return -2;
  }

  int n_len = rate * FRAME_LEN;
  int n_shift = rate * FRAME_SHIFT;

  // Define analyzer
  PitchAnalyzer analyzer(n_len, rate, PitchAnalyzer::RECT, 50, 500, umaxnorm,u1norm,upot);
  /// \TODO
  /// Preprocess the input signal in order to ease pitch estimation. For instance,
  /// central-clipping or low pass filtering may be used.
  /// central-clipping
  auto it = *max_element(x.begin(), x.end());
  float umbral=0.01*it;
  for (int i=0; i < int(x.size()-1); i++) {
    if((umbral*-1<x[i]) && (x[i]<umbral)){
        x[i]=0;
    }
  }
  // Iterate for each frame and save values in f0 vector
  vector<float>::iterator iX;
  vector<float> f0;
   int i=0;
  for (iX = x.begin(); iX + n_len < x.end(); iX = iX + n_shift, i = i + n_shift) {
    float valormax=x[i];
    for(int j=0;j<n_len;j++){
        if(x[j+i]>valormax){
          valormax=x[j+i];
        }
    }
    float umbral2=0.2*valormax;
    for(int j=0;j<n_len;j++){
      if((umbral2*-1<x[i+j]) and (x[i+j]<umbral2)){
        x[i+j]=0;
      }
    }
    float f = analyzer(iX, iX + n_len);
    f0.push_back(f);
  }

  /// \TODO
  /// Postprocess the estimation in order to supress errors. For instance, a median filter
  /// or time-warping may be used.
  /// median filter
  vector<float> f0mediana;
  f0mediana[0]=f0[0];
  //for(int j = 1; j< int(f0.size())-2; j++){
  //  if((f0[j-1]<=f0[j] and f0[j]<=f0[j+1]) or (f0[j+1]<=f0[j] and f0[j]<=f0[j-1])) f0mediana[j]=f0[j];
  //  if((f0[j]<=f0[j-1] and f0[j-1]<=f0[j+1])or (f0[j+1]<=f0[j-1] and f0[j-1]<=f0[j])) f0mediana[j]=f0[j-1];
  //  if((f0[j-1]<=f0[j+1] and f0[j+1]<=f0[j]) or (f0[j]<=f0[j+1] and f0[j+1]<=f0[j-1])) f0mediana[j]=f0[j+1];
  //}
  //f0mediana[int(f0.size())-1]=f0[int(f0.size())-1];

  // Write f0 contour into the output file
  ofstream os(output_txt);
  if (!os.good()) {
    cerr << "Error reading output file " << output_txt << " (" << strerror(errno) << ")\n";
    return -3;
  }

  os << 0 << '\n'; //pitch at t=0
  for (iX = f0.begin(); iX != f0.end(); ++iX) 
    os << *iX << '\n';
  os << 0 << '\n';//pitch at t=Dur

  return 0;
}
