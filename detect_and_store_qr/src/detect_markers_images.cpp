#include <opencv2/opencv.hpp>
#include <opencv2/aruco.hpp>
#include <string>
#include <fstream>
#include <stdio.h>
#include <iostream>

void readDetectorParameters(std::string filename, cv::Ptr<cv::aruco::DetectorParameters> &params) {
  cv::FileStorage fs(filename, cv::FileStorage::READ);
  fs["adaptiveThreshWinSizeMin"] >> params->adaptiveThreshWinSizeMin;
  fs["adaptiveThreshWinSizeMax"] >> params->adaptiveThreshWinSizeMax;
  fs["adaptiveThreshWinSizeStep"] >> params->adaptiveThreshWinSizeStep;
  fs["adaptiveThreshConstant"] >> params->adaptiveThreshConstant;
  fs["minMarkerPerimeterRate"] >> params->minMarkerPerimeterRate;
  fs["maxMarkerPerimeterRate"] >> params->maxMarkerPerimeterRate;
  fs["polygonalApproxAccuracyRate"] >> params->polygonalApproxAccuracyRate;
  fs["minCornerDistanceRate"] >> params->minCornerDistanceRate;
  fs["minDistanceToBorder"] >> params->minDistanceToBorder;
  fs["minMarkerDistanceRate"] >> params->minMarkerDistanceRate;
  fs["cornerRefinementWinSize"] >> params->cornerRefinementWinSize;
  fs["cornerRefinementMaxIterations"] >> params->cornerRefinementMaxIterations;
  fs["cornerRefinementMinAccuracy"] >> params->cornerRefinementMinAccuracy;
  fs["markerBorderBits"] >> params->markerBorderBits;
  fs["perspectiveRemovePixelPerCell"] >> params->perspectiveRemovePixelPerCell;
  fs["perspectiveRemoveIgnoredMarginPerCell"] >> params->perspectiveRemoveIgnoredMarginPerCell;
  fs["maxErroneousBitsInBorderRate"] >> params->maxErroneousBitsInBorderRate;
  fs["minOtsuStdDev"] >> params->minOtsuStdDev;
  fs["errorCorrectionRate"] >> params->errorCorrectionRate;
}

void writeMarkerPositions(std::string file_name, std::vector<cv::Point2f> image_points) {
  cv::FileStorage fs(file_name, cv::FileStorage::WRITE);
  cv::Mat image_points_mat = cv::Mat(image_points.size(), 2, CV_32F, image_points.data());
  fs << "image_positions" << image_points_mat;
  fs.release();
  std::fstream file_in(file_name, std::fstream::in);
  std::fstream file_out("temp.yml", std::fstream::out);
  std::string line;
  while(std::getline(file_in,line)){
    if(line == "---")
      continue;
    file_out << line << "\n";
  }
  file_in.close();
  file_out.close();
  remove(file_name.c_str());
  rename("temp.yml", file_name.c_str());
  std::cout << std::endl << image_points_mat.size().height << " positions of marker with id 0 written to " << file_name << std::endl;
}

int main(int argc, char *argv[]) {

  cv::FileStorage cam_calibration_file;
  cv::Mat K, d;
  // aruco
  cv::Ptr<cv::aruco::DetectorParameters> detectorParams = cv::aruco::DetectorParameters::create();
  std::vector<int> ids;
  std::vector< std::vector< cv::Point2f > > corners;
  std::vector< cv::Point2f > image_points;
  cv::Point2f center;
  // images
  cv::Mat img;
  // file names
  std::string file_name = "../../config/qr_vicon_image_Npoints.yml";
  std::string image_name;

  // read stuffs from configuration and calibration files
  cam_calibration_file.open("../../config/calibration_funstuffs_cam.yml", cv::FileStorage::READ);
  cam_calibration_file["camera_matrix"] >> K;
  cam_calibration_file["distortion_coefficients"] >> d;

  readDetectorParameters("../../config/qr_detector_params.yml", detectorParams);

  // aruco dictionary
  cv::Ptr<cv::aruco::Dictionary> dictionary = cv::aruco::getPredefinedDictionary(
    cv::aruco::PREDEFINED_DICTIONARY_NAME(cv::aruco::DICT_4X4_50)
  );

  cv::namedWindow("image", 0);

  int n = 0;

  while(true) {

    n++;

    image_name = "../../data/qr_vicon_pics/img_" + std::to_string(n) + ".png";
    img = cv::imread(image_name);

    if (img.empty()){
      std::cout << image_name << " is not a valid image file" << std::endl;
      break;
    }

    cv::aruco::detectMarkers(
      img,
      dictionary,
      corners,
      ids,
      detectorParams
    );

    if (std::find(ids.begin(), ids.end(), 0) != ids.end()) {
      for (int i = 0; i < ids.size(); i++) {
        if (ids[i] == 0) {
          center = cv::Point2f(
            0.25*(corners[i][0].x+corners[i][1].x+corners[i][2].x+corners[i][3].x),
            0.25*(corners[i][0].y+corners[i][1].y+corners[i][2].y+corners[i][3].y)
          );
          cv::circle(img, center, 10, cv::Scalar(0,0,255), -1);
        }
      }
      cv::aruco::drawDetectedMarkers(img, corners, ids);
    }

    cv::imshow("image", img);

    if (cv::waitKey() == 27)
      break;

    image_points.push_back(center);
    std::cout << "position " << center << " stored" << std::endl;

  }

  writeMarkerPositions(file_name, image_points);

  return 0;

}
