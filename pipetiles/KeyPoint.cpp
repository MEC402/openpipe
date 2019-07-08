#include <opencv2/opencv.hpp>
#include "opencv2/xfeatures2d.hpp"
#include "opencv2/features2d.hpp"

using namespace std;
using namespace cv;
using namespace cv::xfeatures2d;

const int MAX_FEATURES = 2000;
const float GOOD_MATCH_PERCENT = 0.15f;


void alignImages(Mat &im1, Mat &im2, Mat &im1Reg, Mat &h)

{
	// Convert images to grayscale
	Mat im1Gray, im2Gray;
	cvtColor(im1, im1Gray, COLOR_BGR2GRAY);
	cvtColor(im2, im2Gray, COLOR_BGR2GRAY);

	// Variables to store keypoints and descriptors
	std::vector<KeyPoint> keypoints1, keypoints2;
	Mat descriptors1, descriptors2;

	// CHANGED
	//Detect ORB features and compute descriptors.
	//Ptr<Feature2D> orb = ORB::create(50000);
	//orb->detectAndCompute(im1Gray, Mat(), keypoints1, descriptors1);
	//orb->detectAndCompute(im2Gray, Mat(), keypoints2, descriptors2);
	std::cout << "\tDetecting left keypoints/descriptors..." << std::endl;
	//Ptr<Feature2D> brisk = BRISK::create();
	//brisk->detectAndCompute(im1Gray, Mat(), keypoints1, descriptors1);
	//brisk->detectAndCompute(im2Gray, Mat(), keypoints2, descriptors2);
	Ptr<Feature2D> sift = SIFT::create();
	sift->detectAndCompute(im1Gray, Mat(), keypoints1, descriptors1);
	std::cout << "\tDetecting right keypoints/descriptors..." << std::endl;
	sift->detectAndCompute(im2Gray, Mat(), keypoints2, descriptors2);
	descriptors1.convertTo(descriptors1, CV_32F);
	descriptors2.convertTo(descriptors2, CV_32F);

	//std::cout << "\tDrawing Keypoints..." << std::endl;
	//Mat leftKeypoints;
	//Mat rightKeypoints;
	//drawKeypoints(im1, keypoints1, leftKeypoints );
	//drawKeypoints(im2, keypoints2, rightKeypoints);
	//imwrite("left_keypoints.png", leftKeypoints);
	//imwrite("right_keypoints.png", rightKeypoints);

	// CHANGED
	// Match features.
	std::cout << "\tMatching Descriptors..." << std::endl;
	std::vector<DMatch> matches;
	//Ptr<DescriptorMatcher> matcher = DescriptorMatcher::create("BruteForce-Hamming");
	Ptr<DescriptorMatcher> matcher = FlannBasedMatcher::create();
	matcher->match(descriptors1, descriptors2, matches);

	//FileStorage fs("LeftKeypoints.txt", FileStorage::WRITE);
	//write(fs, "left_keypoints", keypoints1);
	//fs.release();
	//FileStorage fs2("RightKeypoints.txt", FileStorage::WRITE);
	//write(fs2, "right_keypoints", keypoints2);
	//fs2.release();
	//FileStorage fs3("MatchKeypoints.txt", FileStorage::WRITE);
	//write(fs3, "match_keypoints", matches);
	//fs3.release();

	std::cout << "\tSelecting Good Matches..." << std::endl;
	double max_dist = 0; double min_dist = 100;
	for (int i = 0; i < descriptors1.rows; i++)
	{
		double dist = matches[i].distance;
		if (dist < min_dist) min_dist = dist;
		if (dist > max_dist) max_dist = dist;
	}

	std::vector< DMatch > good_matches;
	for (int i = 0; i < descriptors1.rows; i++)
	{
		if (matches[i].distance <= max(2 * min_dist, 0.02))
		{
			good_matches.push_back(matches[i]);
		}
	}

	/*std::vector< DMatch > good_matches;
	for (int i = 0; i < descriptors1.rows; i++)
	{
		if (matches[i].distance <= 200)
		{
			good_matches.push_back(matches[i]);
		}
	}*/

	// Sort matches by score
	std::cout << "\tSorting Matches..." << std::endl;
	std::sort(good_matches.begin(), good_matches.end(), [](DMatch a, DMatch b)
	{return (std::abs(a.distance) < std::abs(b.distance));} );
	//std::sort(matches.begin(), matches.end());
	// std::reverse(matches.begin(), matches.end());

	// Remove not so good matches
	std::vector<KeyPoint> LeftGoodKeypoints, RightGoodKeypoints;
	std::vector< DMatch > TopTenMatches;
	for (int i = 0; i < 10; i++) {
		int i1 = good_matches[i].queryIdx;
		int i2 = good_matches[i].trainIdx;
		CV_Assert(i1 > 0 && i1 < static_cast<int>(keypoints1.size()));
		CV_Assert(i2 > 0 && i2 < static_cast<int>(keypoints2.size()));
		LeftGoodKeypoints.push_back(keypoints1[i1]);
		RightGoodKeypoints.push_back(keypoints2[i2]);
		TopTenMatches.push_back(good_matches[i]);
	}

	std::cout << "\tCalculating Distance..." << std::endl;
	double LeftDistance[10][10];
	double RightDistance[10][10];
	double Ldistance, Rdistance;
	for (int i = 0; i < 10; i++) {
		for (int j = 0; j < 10; j++) {
			Ldistance = sqrt(pow((LeftGoodKeypoints[j].pt.x - LeftGoodKeypoints[i].pt.x),2)
				+ pow((LeftGoodKeypoints[j].pt.y - LeftGoodKeypoints[i].pt.y),2));
			Rdistance = sqrt(pow((RightGoodKeypoints[j].pt.x - RightGoodKeypoints[i].pt.x), 2)
				+ pow((RightGoodKeypoints[j].pt.y - RightGoodKeypoints[i].pt.y), 2));
			LeftDistance[i][j] = Ldistance;
			RightDistance[i][j] = Rdistance;
		}
	}

	/*const int numGoodMatches = matches.size() * GOOD_MATCH_PERCENT;
	matches.erase(matches.begin() + numGoodMatches, matches.end());*/
	FileStorage fs4("GoodKeypoints.txt", FileStorage::WRITE);
	write(fs4, "good_keypoints", good_matches);
	fs4.release();
	FileStorage fs5("leftGoodKeypoints.txt", FileStorage::WRITE);
	write(fs5, "left_good_keypoints", LeftGoodKeypoints);
	fs5.release();
	FileStorage fs6("rightGoodKeypoints.txt", FileStorage::WRITE);
	write(fs6, "right_good_keypoints", RightGoodKeypoints);
	fs6.release();
	FileStorage fs7("TopTenKeypoints.txt", FileStorage::WRITE);
	write(fs7, "top_tent_keypoints", TopTenMatches);
	fs7.release();
	std::ofstream fs8("LeftDistances.csv");
	std::ofstream fs9("RightDistances.csv");

	for (int i = 0; i < 10; i++) {
		for (int j = 0; j < 10; j++) {
			fs8 << std::to_string(LeftDistance[i][j]) <<",";
			fs9 << std::to_string(RightDistance[i][j]) <<",";
		}
		fs8 << "\n";
		fs9 << "\n";
	}

	
	fs8.close();
	fs9.close();

	// Draw top matches
	Mat imMatches;
	Mat TenMatches;
	drawMatches(im1, keypoints1, im2, keypoints2, good_matches, imMatches);
	drawMatches(im1, keypoints1, im2, keypoints2, TopTenMatches, TenMatches);
	// CHANGED
	 imwrite("matches.jpg", imMatches);
	 imwrite("top_ten_matches.jpg", TenMatches);
	//imwrite("matches-brisk-flann.jpg", imMatches);
}


int main(int argc, char **argv)
{
	// Read reference image
	string refFilename(argv[1]);
	cout << "Reading reference image : " << refFilename << endl;
	Mat imReference = imread(refFilename);


	// Read image to be aligned
	string imFilename(argv[2]);
	cout << "Reading image to align : " << imFilename << endl;
	Mat im = imread(imFilename);


	// Registered image will be resotred in imReg. 
	// The estimated homography will be stored in h. 
	Mat imReg, h;

	// Align images
	cout << "Aligning images ..." << endl;
	alignImages(im, imReference, imReg, h);



}