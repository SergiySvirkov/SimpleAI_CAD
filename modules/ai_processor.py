import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import open3d as o3d
import pcl
from torch.utils.data import DataLoader, Dataset
from models.pointnet import PointNetClassifier  # Assuming PointNet model implementation exists

class PointCloudDataset(Dataset):
    def __init__(self, point_clouds, labels):
        self.point_clouds = point_clouds
        self.labels = labels
    
    def __len__(self):
        return len(self.point_clouds)
    
    def __getitem__(self, idx):
        return torch.tensor(self.point_clouds[idx], dtype=torch.float32), torch.tensor(self.labels[idx], dtype=torch.long)

class AIProcessor:
    def __init__(self, model_path='models/pointnet_model.pth'):
        self.model = PointNetClassifier()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.eval()
    
    def preprocess_point_cloud(self, file_path):
        pcd = o3d.io.read_point_cloud(file_path)
        pcd = pcd.voxel_down_sample(voxel_size=0.02)  # Downsample for efficiency
        pcd, _ = pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)  # Denoising
        
        # Convert Open3D format to PCL format for additional processing
        pcl_pcd = pcl.PointCloud()
        pcl_pcd.from_array(np.asarray(pcd.points, dtype=np.float32))
        
        # Apply additional PCL-based filtering
        sor = pcl_pcd.make_statistical_outlier_filter()
        sor.set_mean_k(50)
        sor.set_std_dev_mul_thresh(1.0)
        filtered_pcd = sor.filter()
        
        points = np.asarray(filtered_pcd.to_array())
        if points.shape[0] < 1024:
            points = np.pad(points, ((0, 1024 - points.shape[0]), (0, 0)), mode='constant')  # Padding to 1024 points
        return points[:1024, :3]  # Keep only 1024 points

    def infer(self, file_path):
        points = self.preprocess_point_cloud(file_path)
        points = torch.tensor(points, dtype=torch.float32).unsqueeze(0).to(self.device)
        with torch.no_grad():
            output = self.model(points)
            prediction = torch.argmax(output, dim=1).cpu().numpy()
        return prediction

if __name__ == "__main__":
    ai_processor = AIProcessor()
    result = ai_processor.infer("sample.rcp")
    print(f"Predicted Class: {result}")
